# learn

A Claude Code skill that teaches you things from first principles, and makes sure you actually understand them instead of watching Claude do the work.

You write the code. Claude teaches, asks, hints, reviews, and checks whether your understanding is real. Progress is saved in plain files, so any session can pick up with `/learn continue X`.

## Four modes

| Mode | Give it | You get |
|---|---|---|
| **teach** | a topic, a job description, or school material (slides, syllabus, exam topics) | a study plan built around what you already know, then lessons, exercises, and checks |
| **rebuild** | an existing project (local path or git URL) | the project broken into phases you write yourself, from the simplest working version up |
| **build** | an idea or a project brief | an outline of *problems* you approve, then you design and write each phase |
| **rederive** | a finished project | you re-derive each design decision from the bare problem, then find it in the real code and break it on purpose |

It runs only when you type `/learn`, so it never takes over a quick question or another session. Say what you want after it:

```
/learn teach me RTOS scheduling
/learn here's a job description, build me a study plan: <paste>
/learn help me study for my OS midterm, slides are in ~/courses/os
/learn rebuild ~/code/some-repo
/learn build a resume project: an async job queue in Go
/learn rederive https://github.com/<owner>/<repo>
/learn continue rtos
```

Installed as a plugin, the command may show up as `/learn:learn`.

## How it teaches

- **Why before how.** Each concept opens with what you can't do yet, or what breaks without it.
- **Bridges from what you know.** A short intake records your background once ("you know Python, so here's how C differs") and the plan skips what you already know.
- **Proved by running it.** Demos show real output, including the failures: sanitizer errors, race tests losing, rejected inserts.
- **You write it.** Exercise templates describe each function but don't give its signature. New syntax gets a tiny example that has nothing to do with your task, never the answer.
- **Hints before answers.** Say "check": first a hint, then a narrower hint, then options or the fix with the reason. You retype it and explain why it works.
- **No fake understanding.** Before anything is marked done: predict-the-output questions, explain it as if to an interviewer, and write it from a blank screen. Misses come back as review questions in later sessions.
- **No made-up numbers.** In build mode, every number in your docs or on a resume must come from a run you logged.

## What it creates

Everything lives in one folder per topic, outside your projects:

```
~/learning/
  index.md              every topic and where you are in it
  <topic>/
    profile.md          your background and goals (asked once)
    plan.md             the plan (a hidden answer map in rederive mode)
    progress.md         "you are here", review queue, recurring mistakes, measurements
    notes.md            rules you've learned, in your own words
    practice/           demos and exercises
```

- **It never edits your project repos.** Experiments run in a copy under `~/learning/<topic>/sandbox/`.
- **Topics stay separate.** Two study plans on the same subject (say, two firmware job descriptions) each keep their own plan and progress. What you passed in one shows up in the other as a quick review, never as a skipped lesson or a "go finish it over there".
- Set `LEARN_ROOT` to keep the topics somewhere other than `~/learning`.

## Install

**As a plugin** (easiest to update):

```
/plugin marketplace add aaldelaimy/learn-skill
/plugin install learn@learn-skill
```

**By hand:**

```
git clone https://github.com/aaldelaimy/learn-skill.git
cp -R learn-skill/skills/learn ~/.claude/skills/
```

Requires `git` and `python3`. `skills/learn/scripts/repo_summary.py` summarizes a repo's history and dependency graph using only the Python standard library. It reads Python, Go, JS/TS, Rust, and C/C++.

## Layout

```
skills/learn/
  SKILL.md                     mode routing and the session loop every mode shares
  references/                  one procedure per mode, plus intake and the understanding check
  templates/                   plan, progress, profile, notes, and exercise formats
  scripts/repo_summary.py      repo history and structure summary
```

## License

MIT
