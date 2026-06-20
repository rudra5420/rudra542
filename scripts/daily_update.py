#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              THE CHRONICLE — Daily GitHub Update             ║
║  Zero external dependencies. Set it once. Runs forever.     ║
║  Every element is deterministic — same date = same output.   ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import os
import hashlib
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════
#  DATA — 50 quotes, 52 weekly tips. No external APIs needed.
# ═══════════════════════════════════════════════════════════════

QUOTES = [
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("The most dangerous phrase in the language is 'We've always done it this way.'", "Grace Hopper"),
    ("One of my most productive days was throwing away 1,000 lines of code.", "Ken Thompson"),
    ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
    ("Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.", "Brian W. Kernighan"),
    ("The art of programming is the art of organizing complexity.", "Edsger W. Dijkstra"),
    ("The function of good software is to make the complex appear to be simple.", "Grady Booch"),
    ("Truth can only be found in one place: the code.", "Robert C. Martin"),
    ("Always code as if the person who ends up maintaining your code will be a violent psychopath who knows where you live.", "John F. Woods"),
    ("No one in the brief history of computing has ever written a piece of perfect software.", "Andy Hunt"),
    ("All problems in computer science can be solved by another level of indirection.", "David Wheeler"),
    ("Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away.", "Antoine de Saint-Exupéry"),
    ("There are only two hard things in Computer Science: cache invalidation and naming things.", "Phil Karlton"),
    ("The best code is no code at all.", "Jeff Atwood"),
    ("An idiot admires complexity; a genius admires simplicity.", "Terry A. Davis"),
    ("Measuring programming progress by lines of code is like measuring aircraft building progress by weight.", "Bill Gates"),
    ("Every great developer got there by solving problems they were unqualified to solve — until they did.", "Patrick McKenzie"),
    ("The problem with quick and dirty is that dirty remains long after quick is forgotten.", "Steve McConnell"),
    ("Good judgment comes from experience, and experience comes from bad judgment.", "Frederick P. Brooks"),
    ("Sometimes it pays to stay in bed on Monday rather than spend the rest of the week debugging Monday's code.", "Dan Salomon"),
    ("Beware of bugs in the above code; I have only proved it correct, not tried it.", "Donald Knuth"),
    ("The most powerful tool we have as developers is automation.", "Scott Hanselman"),
    ("Don't document bad code — rewrite it.", "Brian W. Kernighan"),
    ("Design is not just what it looks like and feels like. Design is how it works.", "Steve Jobs"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("Computers are good at following instructions, but not at reading your mind.", "Donald Knuth"),
    ("Simplicity does not precede complexity, but follows it.", "Alan Perlis"),
    ("Write code every day.", "John Resig"),
    ("The competent programmer is fully aware of the limited size of their own skull.", "Edsger W. Dijkstra"),
    ("I'm not a great programmer; I'm just a good programmer with great habits.", "Kent Beck"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("A good programmer looks both ways before crossing a one-way street.", "Doug Linder"),
    ("Controlling complexity is the essence of computer programming.", "Brian W. Kernighan"),
    ("The best way to get a project done faster is to start sooner.", "Jim Highsmith"),
    ("A language that doesn't affect the way you think about programming is not worth knowing.", "Alan Perlis"),
    ("Before software can be reusable, it first has to be usable.", "Ralph Johnson"),
    ("We should forget about small efficiencies: premature optimization is the root of all evil.", "Donald Knuth"),
    ("Deleted code is debugged code.", "Jeff Sickel"),
    ("If it's not tested, it's broken.", "Bruce Eckel"),
    ("Software is a great combination of artistry and engineering.", "Bill Gates"),
    ("The most important skill in software development is communication.", "Martin Fowler"),
    ("Refactoring is paying off technical debt.", "Martin Fowler"),
    ("Good code is its own best documentation.", "Steve McConnell"),
    ("The best programmers are not marginally better than merely good ones. They are an order of magnitude better.", "Randall E. Stross"),
]

TIPS = [
    # Week 01–13: Foundations
    "**Semantic Commits** — Use prefixes like `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`. Your git log becomes self-documenting and enables automated changelogs.",
    "**Git Bisect** — Binary-search through commits to find which one introduced a bug: `git bisect start`, mark bad/good commits, Git guides you in O(log n) steps.",
    "**Const by Default** — In JavaScript/TypeScript, default to `const`. Only escalate to `let` when you know the variable will be reassigned. Fewer moving parts.",
    "**Environment Variables** — Store ALL secrets and config in env vars. Never hardcode API keys or passwords. Use `.env.example` to document required variables.",
    "**Test-Driven Development** — Write the test before the code. It forces clarity on the API and edge cases before you're deep in implementation details.",
    "**Master Your Shortcuts** — Invest one hour learning your IDE's keyboard shortcuts. The compounding productivity effect over a career is enormous.",
    "**Comment the Why** — Code shows *what* it does. Comments should explain *why* — the reasoning, tradeoffs, and non-obvious decisions that aren't visible in code.",
    "**console.table()** — Use `console.table(array)` instead of `console.log()` to inspect arrays of objects. DevTools renders a clean, searchable table.",
    "**Single Responsibility** — Keep functions short enough to fit on one screen without scrolling. If you need to scroll, it likely has more than one job.",
    "**YAGNI** — 'You Ain't Gonna Need It.' Build features when actually needed. Speculative code becomes dead weight and maintenance burden.",
    "**Git Stash** — Use `git stash` to shelve uncommitted changes instantly, switch context, then `git stash pop` to restore. Cleaner than temporary commits.",
    "**Profile First** — Measure before optimizing. Find the actual bottleneck with a profiler. Human intuition about performance hotspots is frequently wrong.",
    "**Boolean Naming** — Prefix booleans with `is`, `has`, `can`, `should`, or `will`: `isLoading`, `hasPermission`, `canDelete`. They read like natural language.",
    # Week 14–26: Architecture
    "**Unix Philosophy** — Do one thing well. A function that accepts a boolean flag to switch behavior is secretly two functions. Split them.",
    "**EditorConfig** — Add `.editorconfig` to every project. It enforces consistent indent style, line endings, and charset across all editors and team members.",
    "**Composition > Inheritance** — Prefer composing small behaviors over deep inheritance hierarchies. Swap components freely without restructuring entire trees.",
    "**Rubber Duck Debug** — Explain your code aloud to an inanimate object. Verbalizing forces different cognitive processing and reveals bugs instantly.",
    "**Feature Flags** — Merge incomplete features behind a toggle instead of long-lived branches. Eliminates catastrophic merge conflicts and enables safe rollouts.",
    "**Learn Regex** — One well-crafted regular expression replaces dozens of lines of string manipulation code. It's a lifetime investment in expressiveness.",
    "**README First** — Write your README before coding. Answering 'what does this do, how do I run it, how do I contribute' clarifies scope before a line of code.",
    "**Gitignore Early** — Create `.gitignore` before your first commit. Removing accidentally tracked files from history requires rewriting every subsequent commit.",
    "**Async/Await** — Prefer `async/await` over raw Promise chains. Sequential visual flow plus natural `try/catch` error handling makes async code readable.",
    "**Pomodoro** — 25 minutes focused work, 5 minute break, long break every 4 cycles. Sustained sessions reduce the cognitive fatigue that produces buggy code.",
    "**Code Review Focus** — In reviews, flag logic errors, security issues, and maintainability. Configure a linter/formatter to handle style — free reviewers for substance.",
    "**Database Indexes** — Add indexes to columns you frequently filter or sort by. An unindexed query on millions of rows can be 1,000× slower than an indexed one.",
    "**DRY vs Abstraction** — DRY is a principle, not a religion. Some duplication is acceptable. The wrong abstraction is far more painful than a little repetition.",
    # Week 27–39: Systems
    "**Learn tmux** — Terminal multiplexer: split panes, multiple windows, detachable sessions that survive SSH disconnects. It changes how you work in terminals.",
    "**Semantic Versioning** — MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Communicate intent to every downstream consumer automatically.",
    "**No DIY Crypto** — Never implement your own cryptography. Cryptographic mistakes are catastrophic, invisible, and usually exploited months after deployment.",
    "**Immutable Config** — Use `Object.freeze()` or TypeScript's `as const` on config objects. Prevents accidental mutation that produces state bugs that are hard to trace.",
    "**Custom Error Types** — Define specific error classes instead of throwing generic `Error`. A well-named error communicates context without requiring a stack trace.",
    "**CSS Custom Properties** — Use variables for design tokens: `--color-primary`, `--spacing-md`, `--radius-sm`. Theming becomes a single-variable change.",
    "**grep / awk / sed** — These Unix tools process gigabytes of logs in seconds. Knowing them is faster than writing a custom script for data extraction tasks.",
    "**Load Test Early** — Load-test before production launches. Systems fail at unexpected scale in ways that unit and integration tests never reveal.",
    "**Idempotent Operations** — Design operations so calling them once or a hundred times produces the same result. Retries, replays, and crash recovery become safe.",
    "**Monorepo Benefits** — Monorepos shine for tightly coupled projects: atomic cross-project refactoring, single PR for related changes, no version coordination.",
    "**Feynman Technique** — Study a concept, then explain it in simple language as if teaching a beginner. Gaps in your understanding surface immediately.",
    "**Connection Pooling** — Never create a new database connection per request. Pooling amortizes connection overhead and routinely delivers 10× throughput.",
    "**Type Your Contracts** — Define API contracts with OpenAPI/Swagger or GraphQL schemas. Living documentation that enables client generation and prevents drift.",
    # Week 40–52: Mastery
    "**Boy Scout Rule** — Always leave code slightly cleaner than you found it. Rename a confusing variable, extract a function, delete dead code. Entropy resists.",
    "**Content-Addressable Cache** — If the content hash matches, the result is identical. This is how Git objects, Docker layers, and npm's lockfile integrity work.",
    "**Know Your GC** — Understanding garbage collector behavior (generational collection, GC pressure, object promotion) helps diagnose mysterious latency spikes.",
    "**Rate Limit From Day One** — Adding rate limits to existing APIs requires coordinating with every existing client. Build them in before anyone depends on the current behavior.",
    "**Branch Naming** — `feat/user-auth`, `fix/login-redirect`, `chore/upgrade-deps`. Readable, filterable, and communicates scope without opening a PR.",
    "**Backpressure** — In data pipelines, let consumers pull at their own pace rather than having producers push. Prevents fast producers from overwhelming slow consumers.",
    "**Write ADRs** — Architecture Decision Records capture *why* a decision was made. Future teammates (including you in 6 months) will be deeply grateful.",
    "**Paginate Everything** — Every list endpoint should paginate from day one. Returning unbounded collections is a memory exhaustion bug waiting for production data.",
    "**Health Checks** — Readiness and liveness probes are mandatory in production. Without them, load balancers happily route requests to starting or crashed instances.",
    "**Know Your DNS** — TTL, record types (A, CNAME, MX, TXT, SRV), propagation delays. DNS is implicated in a surprising percentage of production incidents.",
    "**Separate Error Handling** — Handle errors in distinct blocks, not interleaved with the happy path. Mixed code is how simple logic becomes unreadable.",
    "**Structured Logging** — Log in JSON with consistent fields in production. Enables filtering, alerting, and correlation across services in aggregation tools.",
    "**Annual Reflection** — Review your commits, PRs, and projects from this year. What patterns emerge? What would you do differently? Reflection is how growth compounds.",
]

# ═══════════════════════════════════════════════════════════════
#  CORE UTILITIES
# ═══════════════════════════════════════════════════════════════

def _lcg(state: int) -> int:
    """Linear congruential generator — reproducible pseudo-randomness."""
    return (state * 1664525 + 1013904223) & 0xFFFFFFFF


def _seed(d) -> int:
    """Deterministic seed from a date object — same date always yields same output."""
    return int(hashlib.md5(d.isoformat().encode()).hexdigest(), 16) & 0xFFFFFFFF


def _is_leap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# ═══════════════════════════════════════════════════════════════
#  GENERATORS
# ═══════════════════════════════════════════════════════════════

def year_progress(d):
    """Return (bar_str, pct_float, day_int, total_int, remaining_int)."""
    day   = d.timetuple().tm_yday
    total = 366 if _is_leap(d.year) else 365
    pct   = round((day / total) * 100, 1)
    width = 26
    filled = round((day / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar, pct, day, total, total - day


def constellation(d, width: int = 46, height: int = 4) -> str:
    """
    Generate a unique ASCII star-field for the given date.
    Deterministic: same date → same pattern, always.
    """
    STARS = ["✦", "✧", "⋆", "✺", "∗", "✸", "·", "★"]
    rng = _seed(d)
    grid = [[" "] * width for _ in range(height)]
    placed = set()
    count = 11 + (rng % 7)          # 11–17 stars

    for _ in range(count):
        rng = _lcg(rng);  x = rng % width
        rng = _lcg(rng);  y = rng % height
        rng = _lcg(rng);  star = STARS[rng % len(STARS)]
        if (x, y) not in placed:
            grid[y][x] = star
            placed.add((x, y))

    return "\n".join("".join(row) for row in grid)


def _hsv_to_hex(h: float, s: float, v: float) -> str:
    """Convert HSV (h 0-360, s 0-100, v 0-100) to #RRGGBB hex string."""
    s /= 100; v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    sector = int(h / 60) % 6
    pairs = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]
    r1, g1, b1 = pairs[sector]
    r, g, b = round((r1 + m) * 255), round((g1 + m) * 255), round((b1 + m) * 255)
    return f"#{r:02X}{g:02X}{b:02X}"


_HUE_NAMES = [
    (0,   "Crimson"),    (15,  "Vermilion"),  (30,  "Amber"),
    (50,  "Chartreuse"), (80,  "Forest"),     (120, "Emerald"),
    (155, "Seafoam"),    (175, "Teal"),        (200, "Sky Blue"),
    (220, "Ocean"),      (240, "Indigo"),      (260, "Violet"),
    (280, "Amethyst"),   (300, "Magenta"),     (320, "Rose"),
    (340, "Coral"),      (360, "Crimson"),
]


def _hue_name(h: float) -> str:
    for i in range(len(_HUE_NAMES) - 1):
        if _HUE_NAMES[i][0] <= h < _HUE_NAMES[i + 1][0]:
            return _HUE_NAMES[i][1]
    return "Crimson"


def color_of_day(d):
    """Return (hex_string, color_name) — vibrant, unique to the date."""
    s = _seed(d)
    h = (s >> 16) % 360            # full hue range
    sat = 65 + (s >> 8) % 30       # 65–95 %  (vivid, never washed-out)
    val = 72 + s % 22              # 72–94 %  (bright, never too dark)
    hex_c = _hsv_to_hex(h, sat, val)
    return hex_c, _hue_name(h)


def pick(pool, d, offset: int = 0):
    """Pick deterministically from a pool based on the date."""
    return pool[(_seed(d) + offset) % len(pool)]


# ═══════════════════════════════════════════════════════════════
#  SECTION BUILDER
# ═══════════════════════════════════════════════════════════════

def build_section(d) -> str:
    """Compose the full Chronicle markdown section for date d."""

    bar, pct, day, total, remaining = year_progress(d)
    stars                           = constellation(d)
    hex_c, color_name               = color_of_day(d)
    hex_no_hash                     = hex_c.lstrip("#")
    quote_text, quote_author        = pick(QUOTES, d)
    week_num                        = d.isocalendar()[1]
    tip_text                        = TIPS[(week_num - 1) % len(TIPS)]

    day_names   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day_name  = day_names[d.weekday()]
    month_str = month_names[d.month - 1]
    date_str  = f"{day_name}, {month_str} {d.day} {d.year}"

    # Badge URL for color swatch (shields.io colored badge)
    color_badge = (
        f"https://img.shields.io/badge/"
        f"{color_name.replace(' ', '_')}-{hex_no_hash}"
        f"?style=for-the-badge&color={hex_no_hash}&labelColor={hex_no_hash}"
    )

    section = f"""\
<!-- CHRONICLE:START -->
<div align="center">

---

### ⚡ THE CHRONICLE

**{date_str} · Day {day} of {total}**

---

📅 **Year in Progress**

`{bar}` **{pct}%** — *{remaining} days remaining*

---

🌌 **Constellation #{day}**

```
{stars}
```

---

🎨 **Color of the Day · `{hex_c}` · {color_name}**

[![color swatch]({color_badge})](https://www.color-hex.com/color/{hex_no_hash})

---

💬 **Daily Wisdom**

*"{quote_text}"*

— **{quote_author}**

---

💡 **Tip of the Week · Week {week_num}**

{tip_text}

---

*🤖 Auto-refreshed daily at midnight UTC · Powered by [GitHub Actions](../../actions)*

</div>
<!-- CHRONICLE:END -->"""

    return section


# ═══════════════════════════════════════════════════════════════
#  README WRITER
# ═══════════════════════════════════════════════════════════════

def update_readme(section: str, path: str = "README.md") -> None:
    """
    Replace content between <!-- CHRONICLE:START --> and <!-- CHRONICLE:END -->
    in the target README file. If markers are absent, appends the section.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            original = fh.read()
    except FileNotFoundError:
        original = ""

    pattern = r"<!-- CHRONICLE:START -->.*?<!-- CHRONICLE:END -->"

    if "<!-- CHRONICLE:START -->" in original:
        updated = re.sub(pattern, section, original, flags=re.DOTALL)
    else:
        # Append markers if they don't exist yet
        updated = original.rstrip() + "\n\n" + section + "\n"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(updated)

    print(f"✅  Chronicle updated for {datetime.now(timezone.utc).date()}")


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    today   = datetime.now(timezone.utc).date()
    section = build_section(today)

    readme  = os.getenv("README_PATH", "README.md")
    update_readme(section, readme)
