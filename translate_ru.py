import os
import re
import time
import tarfile
import tempfile
import shutil
import subprocess
from deep_translator import GoogleTranslator

# ============================================================
# Configuration
# ============================================================

SLEEP_TIME = 0.6
MAX_RETRIES = 4
BACKOFF_BASE = 2.0
TOTAL_MODIFIED = 0
TOTAL_TRANSLATED = 0
TOTAL_FAILED = 0

# Original upstream repository. After a fork, URLs containing this
# repository are automatically changed to GITHUB_REPOSITORY.
ORIGINAL_REPO = "snakelair/Keenetic"

# Prefer the repository supplied by GitHub Actions.
# When run locally, fall back to the git remote.
TARGET_REPO = os.environ.get("GITHUB_REPOSITORY", "").strip()


def get_target_repo():
    if TARGET_REPO:
        return TARGET_REPO

    try:
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()

        # Supports:
        #   https://github.com/OWNER/REPO.git
        #   git@github.com:OWNER/REPO.git
        m = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", remote)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
    except Exception:
        pass

    return ORIGINAL_REPO


TARGET_REPO = get_target_repo()

translator = GoogleTranslator(source="auto", target="en")


# ============================================================
# Utility
# ============================================================

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")


def has_cyrillic(text):
    return bool(CYRILLIC_RE.search(text))


def should_skip_translation(text):
    if not text or not text.strip():
        return True

    s = text.strip()

    if not has_cyrillic(s):
        return True

    # URLs / paths / pure symbols
    if re.match(r"^[\W\d]+$", s):
        return True
    if "http://" in s or "https://" in s or "/opt/" in s:
        return True

    if s.lower() in {
        "true", "false", "null", "undefined",
        "var", "let", "const"
    }:
        return True

    return False


def looks_like_error_result(result):
    if not result:
        return True

    s = result.strip().lower()

    # Never allow HTTP/API error text to overwrite source text.
    error_patterns = [
        "error 400",
        "error 401",
        "error 403",
        "error 404",
        "error 408",
        "error 429",
        "error 500",
        "error 502",
        "error 503",
        "error 504",
        "server error",
        "bad gateway",
        "service unavailable",
        "too many requests",
    ]

    return any(p in s for p in error_patterns)


def do_translate(text):
    global TOTAL_TRANSLATED, TOTAL_FAILED

    if should_skip_translation(text):
        return text

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = translator.translate(text)

            if looks_like_error_result(result):
                raise RuntimeError(f"Invalid translation result: {result!r}")

            result = result.strip()

            if not result:
                raise RuntimeError("Empty translation result")

            time.sleep(SLEEP_TIME)
            TOTAL_TRANSLATED += 1
            print(
                f"      [Trans] {text[:40]}... -> {result[:40]}..."
            )
            return result

        except Exception as exc:
            last_error = exc
            print(
                f"      [Translate error {attempt}/{MAX_RETRIES}] "
                f"{exc}"
            )

            if attempt < MAX_RETRIES:
                delay = BACKOFF_BASE ** (attempt - 1)
                time.sleep(delay)

    TOTAL_FAILED += 1
    print(
        f"      [Keep original] translation failed after "
        f"{MAX_RETRIES} attempts: {text[:60]}..."
    )
    return text


def read_file_content(file_path):
    encodings = ["utf-8", "windows-1251", "cp1251", "latin1"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.readlines(), enc
        except UnicodeDecodeError:
            continue
        except OSError:
            return None, None

    return None, None


# ============================================================
# Fork URL replacement
# ============================================================

def replace_fork_urls(text):
    """
    Change links such as:
      https://github.com/snakelair/Keenetic/...
      https://raw.githubusercontent.com/snakelair/Keenetic/...

    to the current fork:
      https://github.com/<current-owner>/Keenetic/...
      https://raw.githubusercontent.com/<current-owner>/Keenetic/...

    Only the repository portion is changed. Paths, branches and
    filenames remain untouched.
    """
    if not TARGET_REPO or TARGET_REPO == ORIGINAL_REPO:
        return text, False

    old_owner, old_name = ORIGINAL_REPO.split("/", 1)
    new_owner, new_name = TARGET_REPO.split("/", 1)

    patterns = [
        (
            rf"(https?://github\.com/){re.escape(old_owner)}/"
            rf"{re.escape(old_name)}(?=/|$)",
            rf"\g<1>{new_owner}/{new_name}",
        ),
        (
            rf"(https?://raw\.githubusercontent\.com/){re.escape(old_owner)}/"
            rf"{re.escape(old_name)}(?=/|$)",
            rf"\g<1>{new_owner}/{new_name}",
        ),
    ]

    changed = False
    result = text

    for pattern, replacement in patterns:
        result2 = re.sub(pattern, replacement, result)
        if result2 != result:
            changed = True
            result = result2

    return result, changed


# ============================================================
# Protected Markdown fragments
# ============================================================

def translate_markdown_text(text):
    """
    Translate human-readable Markdown text while protecting:
      - inline code
      - URLs
      - Markdown link destinations
      - images
      - HTML tags
    """
    if not has_cyrillic(text):
        return text

    protected = []

    def protect(value):
        token = f"@@@PROTECTED_{len(protected)}@@@"
        protected.append(value)
        return token

    # Inline code
    text = re.sub(r"`[^`\n]+`", lambda m: protect(m.group(0)), text)

    # Markdown images: protect the complete image syntax
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        lambda m: protect(m.group(0)),
        text,
    )

    # Markdown links: protect destination, translate visible text later
    link_placeholders = []

    def protect_link(match):
        label = match.group(1)
        destination = match.group(2)
        token = f"@@@LINK_DEST_{len(link_placeholders)}@@@"
        link_placeholders.append(destination)
        return f"[{label}]({token})"

    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        protect_link,
        text,
    )

    # URLs
    text = re.sub(
        r"https?://[^\s<>)]+",
        lambda m: protect(m.group(0)),
        text,
    )

    # HTML tags
    text = re.sub(
        r"<[^>\n]+>",
        lambda m: protect(m.group(0)),
        text,
    )

    translated = do_translate(text)

    # Restore link destinations
    for i, destination in enumerate(link_placeholders):
        translated = translated.replace(
            f"@@@LINK_DEST_{i}@@@",
            destination,
        )

    # Restore all other protected fragments
    for i, value in enumerate(protected):
        translated = translated.replace(
            f"@@@PROTECTED_{i}@@@",
            value,
        )

    return translated


# ============================================================
# Mermaid
# ============================================================

MERMAID_START_RE = re.compile(
    r"^\s*(flowchart|graph|mindmap|sequenceDiagram|stateDiagram(?:-v2)?|"
    r"classDiagram|erDiagram|journey|timeline|gitGraph)\b",
    re.IGNORECASE,
)


def translate_mermaid_line(line):
    """
    Translate visible text in common Mermaid constructs without
    translating Mermaid keywords, IDs, arrows or syntax.

    This intentionally uses conservative patterns. If a line is not
    recognized safely, it is left unchanged rather than risking
    diagram corruption.
    """
    original = line
    newline = "\n" if line.endswith("\n") else ""
    s = line[:-1] if newline else line

    if not has_cyrillic(s):
        return original

    # Mermaid comments: do not translate syntax, but translate comment text.
    if s.lstrip().startswith("%%"):
        prefix = s[:s.index("%%") + 2]
        content = s[s.index("%%") + 2:]
        if has_cyrillic(content):
            return prefix + translate_markdown_text(content) + newline
        return original

    # Node/edge quoted labels: ["..."], {"..."}, ("..."), (("...")),
    # and edge labels |"..."|.
    patterns = [
        (r'(\[\s*")([^"]+)(?="\s*\])', 1),
        (r'(\{\s*")([^"]+)(?="\s*\})', 1),
        (r'(\(\s*")([^"]+)(?="\s*\))', 1),
        (r'(\(\(\s*")([^"]+)(?="\s*\)\))', 1),
        (r'(\|\s*")([^"]+)(?="\s*\|)', 1),
    ]

    result = s

    for pattern, _ in patterns:
        result = re.sub(
            pattern,
            lambda m: m.group(1)
            + translate_markdown_text(m.group(2))
            + result[m.end(2):m.end(2)]  # no-op, keeps replacement simple
            if False else m.group(1) + translate_markdown_text(m.group(2)),
            result,
        )

    # Mermaid also permits unquoted subgraph titles:
    # subgraph Mode1 ["Title"]
    # The quoted-title patterns above already handle this.

    # Root mindmap labels and other conservative bare labels:
    # Only translate lines which are indented and consist of text, not
    # known Mermaid syntax/IDs. This handles common:
    #   mindmap
    #     Русский текст
    if result == s:
        stripped = s.strip()
        indent = s[:len(s) - len(s.lstrip())]

        if (
            stripped
            and indent
            and not re.match(
                r"^(subgraph|end|flowchart|graph|mindmap|"
                r"sequenceDiagram|classDiagram|stateDiagram|erDiagram)\b",
                stripped,
                re.IGNORECASE,
            )
            and not re.search(r"(-->|---|==>|-.->|~~~|\|)", stripped)
            and re.match(r"^[A-Za-zА-Яа-яЁё0-9 _.,:;!?()«»'\"/&+–—-]+$", stripped)
        ):
            result = indent + translate_markdown_text(stripped)

    return result + newline


def process_mermaid_block(block_lines):
    new_lines = []
    modified = False

    for line in block_lines:
        new_line = translate_mermaid_line(line)

        # Also perform fork URL replacement inside Mermaid text.
        new_line, url_changed = replace_fork_urls(new_line)

        if new_line != line:
            modified = True

        if url_changed:
            modified = True

        new_lines.append(new_line)

    return new_lines, modified


# ============================================================
# HTML
# ============================================================

def process_html_lines(lines, modified_flag):
    new_lines = []

    tag_text_pattern = re.compile(r"(>)([^<]+?)(<)")
    attr_names = (
        r"title|alt|placeholder|value|label|content|"
        r"data-title|data-tooltip|data-content|aria-label"
    )
    attr_pattern = re.compile(
        r"\b(" + attr_names + r")=([\"\'])(.*?)([\"\'])"
    )
    comment_pattern = re.compile(r"(<!--\s*)(.*?)(\s*-->)")

    for line in lines:
        # Replace upstream repository URLs first.
        line2, url_changed = replace_fork_urls(line)
        if url_changed:
            modified_flag[0] = True
        line = line2

        def replace_tag(match):
            p, c, s = match.groups()
            if has_cyrillic(c):
                translated = do_translate(c)
                if translated != c:
                    modified_flag[0] = True
                return f"{p}{translated}{s}"
            return match.group(0)

        line = tag_text_pattern.sub(replace_tag, line)

        def replace_attr(match):
            k, q1, c, q2 = match.groups()
            if has_cyrillic(c):
                translated = do_translate(c)
                if translated != c:
                    modified_flag[0] = True
                return f"{k}={q1}{translated}{q2}"
            return match.group(0)

        line = attr_pattern.sub(replace_attr, line)

        def replace_comment(match):
            p, c, s = match.groups()
            if has_cyrillic(c):
                translated = do_translate(c)
                if translated != c:
                    modified_flag[0] = True
                return f"{p}{translated}{s}"
            return match.group(0)

        line = comment_pattern.sub(replace_comment, line)

        new_lines.append(line)

    return new_lines


# ============================================================
# Markdown
# ============================================================

def process_md_lines(lines, modified_flag):
    new_lines = []
    in_code_block = False
    mermaid_block = False
    mermaid_lines = []

    for line in lines:
        stripped = line.strip()

        # Fence handling
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                mermaid_block = stripped.lower().startswith("```mermaid")

                # Fork URL replacement on the fence line is harmless.
                line2, changed = replace_fork_urls(line)
                if changed:
                    modified_flag[0] = True

                new_lines.append(line2)
            else:
                if mermaid_block:
                    translated_block, changed = process_mermaid_block(
                        mermaid_lines
                    )
                    new_lines.extend(translated_block)
                    if changed:
                        modified_flag[0] = True
                    mermaid_lines = []

                mermaid_block = False
                in_code_block = False

                line2, changed = replace_fork_urls(line)
                if changed:
                    modified_flag[0] = True

                new_lines.append(line2)

            continue

        if in_code_block:
            if mermaid_block:
                mermaid_lines.append(line)
            else:
                # Ordinary code blocks are never translated.
                line2, changed = replace_fork_urls(line)
                if changed:
                    modified_flag[0] = True
                new_lines.append(line2)
            continue

        # Outside code blocks.
        line2, url_changed = replace_fork_urls(line)
        if url_changed:
            modified_flag[0] = True
        line = line2

        if not stripped or stripped.startswith("<"):
            new_lines.append(line)
            continue

        if has_cyrillic(line):
            # Markdown heading/list/quote prefix.
            prefix_match = re.match(
                r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s+))(.*)$",
                line.rstrip("\n"),
            )

            if prefix_match:
                prefix, content = prefix_match.groups()
                translated = translate_markdown_text(content)
                result = f"{prefix}{translated}\n"

                if result != line:
                    modified_flag[0] = True

                new_lines.append(result)
                continue

            # Table row: translate each cell separately.
            if "|" in line:
                raw = line.rstrip("\n")
                cells = raw.split("|")
                translated_cells = []

                for cell in cells:
                    if has_cyrillic(cell):
                        translated_cells.append(
                            translate_markdown_text(cell)
                        )
                    else:
                        translated_cells.append(cell)

                result = "|".join(translated_cells) + "\n"
                if result != line:
                    modified_flag[0] = True
                new_lines.append(result)
                continue

            translated = translate_markdown_text(line.rstrip("\n"))
            result = translated + "\n"

            if result != line:
                modified_flag[0] = True

            new_lines.append(result)
            continue

        new_lines.append(line)

    # Defensive handling for malformed/unclosed Mermaid fences.
    if mermaid_lines:
        translated_block, changed = process_mermaid_block(mermaid_lines)
        new_lines.extend(translated_block)
        if changed:
            modified_flag[0] = True

    return new_lines


# ============================================================
# Scripts / JS / JSON / XML / CSS / shell
# ============================================================

def process_script_lines(lines, modified_flag):
    new_lines = []

    string_pattern = re.compile(r'(["\'])(.*?)(["\'])')
    comment_pattern = re.compile(r"^(.*?)(#\s*|//\s*)(.*)$")

    for line in lines:
        line2, url_changed = replace_fork_urls(line)
        if url_changed:
            modified_flag[0] = True
        line = line2

        if line.strip().startswith("#!"):
            new_lines.append(line)
            continue

        match_comment = comment_pattern.match(line)

        if match_comment:
            pre, mark, content = match_comment.groups()

            if has_cyrillic(content):
                translated = do_translate(content.rstrip("\n"))
                ending = "\n" if content.endswith("\n") else ""
                result = f"{pre}{mark}{translated}{ending}"

                if result != line:
                    modified_flag[0] = True

                line = result

        def replace_str(match):
            q1, content, q2 = match.groups()

            if has_cyrillic(content) and "`" not in content:
                translated = do_translate(content)

                if translated != content:
                    modified_flag[0] = True

                return f"{q1}{translated}{q2}"

            return match.group(0)

        line = string_pattern.sub(replace_str, line)
        new_lines.append(line)

    return new_lines


# ============================================================
# File processing
# ============================================================

def process_single_file(file_path, inside_tar=False):
    global TOTAL_MODIFIED

    prefix_log = "    " if inside_tar else ""

    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    script_exts = [
        ".sh", ".cfg", ".conf", ".list", ".txt", ".json",
        ".xml", ".lua", ".js", ".css", ".jsx", ".ts"
    ]
    html_exts = [".html", ".htm", ".asp", ".php"]
    md_exts = [".md", ".markdown"]
    valid_names = ["config", "Makefile", "control", "postinst", "prerm"]

    is_script = (
        any(file_path.endswith(e) for e in script_exts)
        or filename in valid_names
    )
    is_html = ext in html_exts
    is_md = ext in md_exts

    if not (is_script or is_html or is_md):
        return False

    if inside_tar:
        print(f"{prefix_log}Checking: {filename}")

    lines, encoding = read_file_content(file_path)

    if not lines:
        return False

    modified_flag = [False]

    if is_html:
        new_lines = process_html_lines(lines, modified_flag)
    elif is_md:
        new_lines = process_md_lines(lines, modified_flag)
    else:
        new_lines = process_script_lines(lines, modified_flag)

    if modified_flag[0]:
        print(f"{prefix_log}-> Modified: {filename}")

        with open(file_path, "w", encoding=encoding, newline="") as f:
            f.writelines(new_lines)

        TOTAL_MODIFIED += 1
        return True

    return False


# ============================================================
# TAR processing
# ============================================================

def process_tar_file(file_path):
    print(f"📦 Found Archive: {file_path}")

    temp_dir = tempfile.mkdtemp()
    modified_in_tar = False

    try:
        with tarfile.open(file_path, "r:*") as tar:

            def no_owners(members):
                for member in members:
                    member.uid = 0
                    member.gid = 0
                    member.uname = ""
                    member.gname = ""
                    yield member

            tar.extractall(
                path=temp_dir,
                members=no_owners(tar)
            )

        print("  -> Extracted. Scanning internal files...")

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                inner_path = os.path.join(root, file)

                if process_single_file(
                    inner_path,
                    inside_tar=True
                ):
                    modified_in_tar = True

        if modified_in_tar:
            print(f"  -> Repacking: {file_path}")

            if file_path.endswith((".tar.gz", ".tgz")):
                mode = "w:gz"
            else:
                mode = "w"

            with tarfile.open(file_path, mode) as tar:
                tar.add(temp_dir, arcname="")

        else:
            print("  -> No changes inside archive.")

    except Exception as exc:
        print(f"  [Error tar] {exc}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 70)
    print("Russian -> English translation")
    print(f"Original repository : {ORIGINAL_REPO}")
    print(f"Target repository   : {TARGET_REPO}")
    print("=" * 70)

    exclude_dirs = [".git", ".github"]

    for root, dirs, files in os.walk("."):
        dirs[:] = [
            d for d in dirs
            if d not in exclude_dirs
        ]

        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith((".tar", ".tar.gz", ".tgz")):
                process_tar_file(file_path)
            else:
                process_single_file(file_path)

    print("\n" + "=" * 70)
    print(f"Modified files : {TOTAL_MODIFIED}")
    print(f"Translations   : {TOTAL_TRANSLATED}")
    print(f"Failed         : {TOTAL_FAILED}")
    print("=" * 70)

    if TOTAL_FAILED:
        print(
            "⚠ Some translations failed. "
            "Original Russian text was preserved."
        )

    print("✅ All Done.")


if __name__ == "__main__":
    main()
