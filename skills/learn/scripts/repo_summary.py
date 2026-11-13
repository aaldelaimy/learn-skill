#!/usr/bin/env python3
"""Summarize a repository so a teacher can find its design decisions and build order.

Usage: python3 -I repo_summary.py <repo path>

Prints, with every list capped so the output fits in context:
  1. History (when the folder is a git repo): size, first commits, the commits that
     touched the most source files, commits whose message suggests a design change,
     and the files changed most often.
  2. Docs worth reading first.
  3. Layout and languages.
  4. Entry points (where execution starts).
  5. The internal dependency graph: which files everything leans on (fan-in),
     which files pull everything together (fan-out), and the links between them.
  6. Declared external dependencies (from manifests).
Languages: Python, Go, JavaScript/TypeScript, Rust, C/C++. Standard library only.
"""
import ast
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target", ".next", "__pycache__",
             ".venv", "venv", "env", "third_party", ".pytest_cache", ".mypy_cache", "coverage", ".idea", ".vscode"}
SKIP_FILE = re.compile(r"(\.lock|-lock\.json|\.sum|\.min\.(js|css)|\.map|\.snap|\.svg|\.png|\.jpe?g|\.gif|\.pdf|\.ico|\.d\.ts)$")
TEST_FILE = re.compile(r"(^|/)(tests?|__tests__|spec|e2e)/|(^|/)test_[^/]+$|_test\.(go|py|c|cc|cpp)$|\.(test|spec)\.[jt]sx?$")
LANG = {".py": "python", ".go": "go", ".js": "js", ".jsx": "js", ".mjs": "js", ".cjs": "js", ".ts": "js",
        ".tsx": "js", ".rs": "rust", ".c": "c", ".h": "c", ".cc": "c", ".cpp": "c", ".cxx": "c", ".hpp": "c", ".hh": "c"}
DESIGN_WORDS = re.compile(r"\b(introduc|refactor|rewrit|replac|migrat|switch|redesign|architect|instead|extract|split|"
                          r"remov|drop|deprecat|perf|optimi|cache|async|concurren|race|lock|retry|schema|protocol|"
                          r"fix(es|ed)? .*(bug|leak|crash|race|deadlock)|postmortem)", re.I)


def run(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=60).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def read(rel, limit=300_000):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def section(title):
    print(f"\n## {title}")


# ---------- collect files ----------
is_git = run("git", "rev-parse", "--is-inside-work-tree").strip() == "true"
if is_git:
    files = [f for f in run("git", "ls-files").splitlines() if f]
else:
    files = []
    for here, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for n in names:
            files.append(os.path.relpath(os.path.join(here, n), ROOT))
files = [f for f in files if not set(f.split("/")[:-1]) & SKIP_DIRS and not SKIP_FILE.search(f)]
fileset = set(files)
hidden = re.compile(r"(^|/)\.(?!github/)[^/]+/")
code = [f for f in files if os.path.splitext(f)[1] in LANG and not hidden.search(f)]
nloc = {f: read(f).count("\n") for f in code}

# ---------- 1. history ----------
section("History")
if not is_git:
    print("Not a git repo: no history. Read the decisions from the code and docs below.")
else:
    total = run("git", "rev-list", "--count", "HEAD").strip() or "0"
    dates = run("git", "log", "--format=%ad", "--date=short").split()
    authors = len(set(run("git", "log", "--format=%ae").split()))
    head = run("git", "rev-parse", "--short", "HEAD").strip()
    print(f"commits: {total} | {dates[-1] if dates else '?'} to {dates[0] if dates else '?'} | authors: {authors} | HEAD: {head}")
    if run("git", "rev-parse", "--is-shallow-repository").strip() == "true":
        print("WARNING: shallow clone; run `git fetch --unshallow` for the early history")

    log = run("git", "log", "--no-merges", "--date=short", "--format=\x01%h %ad %s", "--name-only")
    commits = []  # (header, [files])
    for block in log.split("\x01")[1:]:
        lines = [l for l in block.splitlines() if l.strip()]
        commits.append((lines[0], lines[1:]))

    print("\nFirst commits (oldest first):")
    for h, _ in list(reversed(commits))[:12]:
        print("  " + h)

    def weight(fs):
        return sum(1 for f in fs if os.path.splitext(f)[1] in LANG and not TEST_FILE.search(f) and not SKIP_FILE.search(f))

    big = sorted(commits, key=lambda c: -weight(c[1]))[:12]
    print("\nCommits touching the most source files (tests and generated files ignored):")
    for h, fs in big:
        if weight(fs):
            print(f"  {weight(fs):3d} files  {h}")

    design = [h for h, _ in commits if DESIGN_WORDS.search(h.split(" ", 2)[-1])][:30]
    print("\nCommits whose message suggests a design change (newest first):")
    print("\n".join("  " + h for h in design) or "  none")

    churn = Counter() if len(commits) < 5 else Counter(f for _, fs in commits for f in fs if f in fileset and not SKIP_FILE.search(f))
    if churn:
        print("\nFiles changed most often:")
    for f, n in churn.most_common(15):
        print(f"  {n:3d}  {f}")

# ---------- 2. docs ----------
section("Docs to read first")
docs = [f for f in files if re.search(r"(^|/)(readme|architecture|design|adr|notes|postmortem|contributing)[^/]*\.(md|rst|txt)$", f, re.I)
        or (f.startswith("docs/") and f.endswith(".md"))]
print("\n".join("  " + d for d in sorted(docs, key=lambda d: (d.count("/"), d))[:20]) or "  none")

# ---------- 3. layout ----------
section("Layout and languages")
top = Counter(f.split("/")[0] + ("/" if "/" in f else "") for f in files)
for d, n in sorted(top.items(), key=lambda kv: -kv[1])[:15]:
    print(f"  {n:4d}  {d}")
langs = Counter(LANG[os.path.splitext(f)[1]] for f in code)
tests = sum(1 for f in code if TEST_FILE.search(f))
print(f"source files: {len(code)} ({tests} tests) | " + ", ".join(f"{l} {n}" for l, n in langs.most_common()))

# ---------- 4 + 5. entry points and dependency graph ----------
edges = defaultdict(set)   # node -> nodes it depends on (nodes are files; Go packages are dirs ending in "/")
entries = []
src = [f for f in code if not TEST_FILE.search(f)]

# Python: build a module index from paths, then resolve imports parsed with ast.
py_mods = {}
for f in src:
    if f.endswith(".py"):
        mod = f[:-3].replace("/", ".")
        if mod.endswith(".__init__"):
            mod = mod[: -len(".__init__")]
        py_mods[mod] = f
        if mod.startswith("src."):
            py_mods[mod[4:]] = f


def py_resolve(name):
    while name:
        if name in py_mods:
            return py_mods[name]
        name = name.rpartition(".")[0]
    return None


# Go: package directory -> files.
go_module = (re.search(r"^module\s+(\S+)", read("go.mod"), re.M) or [None, ""])[1] if "go.mod" in fileset else ""
go_dirs = {os.path.dirname(f) for f in src if f.endswith(".go")}

JS_SPEC = re.compile(r"""(?:from\s*|import\s*\(\s*|require\s*\(\s*|^\s*import\s+)['"]([^'"]+)['"]""", re.M)
JS_EXTS = [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"]
C_INC = re.compile(r'^\s*#\s*include\s*"([^"]+)"', re.M)
RS_MOD = re.compile(r"^\s*(?:pub\s+)?mod\s+(\w+)\s*;", re.M)
RS_USE = re.compile(r"\buse\s+crate::(\w+)")

aliases = []  # (prefix, directory)
for cfg in [f for f in files if os.path.basename(f) in ("tsconfig.json", "jsconfig.json")]:
    text = re.sub(r"//.*", "", read(cfg))
    for alias, target in re.findall(r'"([^"*]+)\*"\s*:\s*\[\s*"([^"*]*)\*?"', text):
        aliases.append((alias, os.path.normpath(os.path.join(os.path.dirname(cfg), target)) if target.strip("./") else os.path.dirname(cfg)))
manifests = [f for f in files if os.path.basename(f) == "package.json" and f.count("/") <= 2]

by_base = defaultdict(list)
for f in src:
    by_base[os.path.basename(f)].append(f)

for f in src:
    lang, text, here = LANG[os.path.splitext(f)[1]], read(f), os.path.dirname(f)
    if lang == "python":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            tree = None
        if tree:
            pkg = py_mods and f[:-3].replace("/", ".").rpartition(".")[0]
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    base = node.module or ""
                    if node.level:
                        parts = pkg.split(".") if pkg else []
                        parts = parts[: len(parts) - (node.level - 1)] if node.level > 1 else parts
                        base = ".".join(p for p in parts + ([base] if base else []) if p)
                    names = [f"{base}.{a.name}" for a in node.names] + [base]
                for n in names:
                    hit = py_resolve(n)
                    if hit and hit != f:
                        edges[f].add(hit)
                        break
        if ('if __name__ == "__main__"' in text or "if __name__ == '__main__'" in text or f.endswith("__main__.py")
                or re.search(r"^\w+\s*=\s*(FastAPI|Flask|Starlette|Django)\(", text, re.M)):
            entries.append(f)
    elif lang == "go":
        node = here + "/"
        block = re.findall(r"import\s*\(([^)]*)\)", text, re.S)
        specs = re.findall(r'"([^"]+)"', " ".join(block)) + re.findall(r'^import\s+(?:\w+\s+)?"([^"]+)"', text, re.M)
        for s in specs:
            if go_module and (s == go_module or s.startswith(go_module + "/")):
                d = s[len(go_module):].lstrip("/")
                if d in go_dirs and d + "/" != node:
                    edges[node].add(d + "/")
        if re.search(r"^package main\b", text, re.M) and re.search(r"^func main\(\)", text, re.M):
            entries.append(f)
    elif lang == "js":
        for s in JS_SPEC.findall(text):
            base = None
            if s.startswith("."):
                base = os.path.normpath(os.path.join(here, s))
            for prefix, d in aliases:
                if s.startswith(prefix):
                    base = os.path.normpath(os.path.join(d, s[len(prefix):]))
            if base:
                for c in [base] + [base + e for e in JS_EXTS] + [base + "/index" + e for e in JS_EXTS]:
                    if c in fileset and c != f and os.path.splitext(c)[1] in LANG:
                        edges[f].add(c)
                        break
        if re.search(r"(^|/)(app|pages)/(.*/)?(page|layout|_app|index)\.[jt]sx?$", f) or re.search(r"(^|/)(server|index|main)\.[jt]s$", f):
            entries.append(f)
    elif lang == "rust":
        for m in RS_MOD.findall(text):
            for c in (os.path.join(here, m + ".rs"), os.path.join(here, m, "mod.rs")):
                if os.path.normpath(c) in fileset:
                    edges[f].add(os.path.normpath(c))
        for m in RS_USE.findall(text):
            for c in (f"src/{m}.rs", f"src/{m}/mod.rs"):
                if c in fileset and c != f:
                    edges[f].add(c)
        if f.endswith("src/main.rs") or "/bin/" in f:
            entries.append(f)
    elif lang == "c":
        for s in C_INC.findall(text):
            c = os.path.normpath(os.path.join(here, s))
            hit = c if c in fileset else (by_base.get(os.path.basename(s)) or [None])[0]
            if hit and hit != f:
                edges[f].add(hit)
        if re.search(r"\bint\s+main\s*\(", text):
            entries.append(f)

for man in manifests:
    try:
        pkg = json.loads(read(man))
        for k in ("main", "module"):
            if isinstance(pkg.get(k), str):
                entries.append(f"{man} {k}: {pkg[k]}")
        b = pkg.get("bin")
        entries += [f"{man} bin: {v}" for v in ([b] if isinstance(b, str) else list((b or {}).values()))]
        entries += [f"{man} script {k}: {v[:80]}" for k, v in list(pkg.get("scripts", {}).items())[:4]]
    except ValueError:
        pass

section("Entry points (where execution starts)")
for e in entries[:15]:
    print(f"  {e}" + (f" ({nloc[e]} lines)" if e in nloc else ""))
if not entries:
    print("  none found; start from the files with the highest fan-out below")


def size(node):
    if node.endswith("/"):
        return f"{sum(nloc[f] for f in src if os.path.dirname(f) + '/' == node)} lines, package"
    return f"{nloc.get(node, 0)} lines"


fan_in = Counter(t for ts in edges.values() for t in ts)
fan_out = {n: len(ts) for n, ts in edges.items() if ts}
section("Most depended on (fan-in): shared core, usually the data model and state")
for n, k in fan_in.most_common(12):
    print(f"  {k:3d}  {n} ({size(n)})")
if not fan_in:
    print("  no internal dependencies found")
section("Depends on the most (fan-out): orchestrators, usually the main flow")
for n, k in sorted(fan_out.items(), key=lambda kv: -kv[1])[:10]:
    print(f"  {k:3d}  {n} ({size(n)})")

central = {n for n, _ in fan_in.most_common(10)} | {n for n, _ in sorted(fan_out.items(), key=lambda kv: -kv[1])[:6]}
section("Links among the central files")
shown = 0
for n in sorted(central):
    ts = sorted(t for t in edges.get(n, ()) if t in central)
    if ts and shown < 20:
        print(f"  {n} -> {', '.join(ts)}")
        shown += 1

section("Largest source files")
for f in sorted(src, key=lambda f: -nloc[f])[:10]:
    print(f"  {nloc[f]:5d}  {f}")

# ---------- 6. external dependencies ----------
section("Declared external dependencies")
deps = []
if go_module:
    deps += [m for m in re.findall(r"^\s*([\w.\-]+/[\w./\-]+)\s+v[\d.]", read("go.mod"), re.M)][:15]
if "pyproject.toml" in fileset:
    m = re.search(r"^dependencies\s*=\s*\[(.*?)\]", read("pyproject.toml"), re.S | re.M)
    deps += re.findall(r'"([A-Za-z0-9_.\-]+)', m.group(1)) if m else []
if "requirements.txt" in fileset:
    deps += [l.split("=")[0].split(">")[0].split("<")[0].strip() for l in read("requirements.txt").splitlines() if l.strip() and not l.startswith("#")]
for man in manifests:
    try:
        deps += list(json.loads(read(man)).get("dependencies", {}))
    except ValueError:
        pass
if "Cargo.toml" in fileset:
    m = re.search(r"^\[dependencies\](.*?)(^\[|\Z)", read("Cargo.toml"), re.S | re.M)
    deps += re.findall(r"^([\w\-]+)\s*=", m.group(1), re.M) if m else []
c_sys = Counter(s for f in src if LANG[os.path.splitext(f)[1]] == "c" for s in re.findall(r"#\s*include\s*<([^>]+)>", read(f)))
deps += [f"<{h}>" for h, _ in c_sys.most_common(12)]
print("  " + (", ".join(dict.fromkeys(deps)) if deps else "none declared"))
