# Rebuild mode

The user writes an existing project again themselves, phase by phase, until they can rebuild and explain the whole thing without looking. The input is an existing project (path or repo URL). For a project that doesn't exist yet, use `references/build.md`.

## Hard rules

- **Never edit the original project.** Read it only. If it's a URL, clone it into `~/learning/<slug>/source/` with `git clone --filter=blob:none`.
- **The user's new code lives in their own folder.** Ask where and record it in `profile.md`. Don't create or edit files there unless the user approves that specific file (for example "yes, scaffold compose.yml"). Reading and reviewing their files is always fine.
- **Never hand over finished files.** Small steps, their keystrokes.
- The user decides when to commit.

## A. Read the original and plan the phases

1. Run `python3 -I scripts/repo_summary.py <repo>` (the path is relative to this skill's folder). Read the README, design docs, and entry points. Follow the imports outward.
2. Write the root problem in one sentence: why the system exists.
3. **Phases ordered by dependency, simplest working version first.** Each phase leaves something that runs. The usual shape:
   - core data model and its rules, with tests
   - smallest useful interface (an API or CLI) over an in-memory store
   - **concept-only phases** before any phase that needs a new runtime model (asyncio, threads, sockets). These are small throwaway experiments in `practice/`, not polished and not added to the project.
   - persistence (by hand first: raw SQL in psql, then the library)
   - the hard core of the system (workers, claiming, retries, recovery)
   - extras, in order of how much they teach (caching, idempotency, shutdown, observability)
   - tests against real dependencies, then CI
4. For each phase, write:
   - what it adds
   - what breaks without it, which is why it comes next
   - the concepts to teach first (any passed in another topic become `[R]` review items: a short check, and a miss becomes a full lesson)
   - 3–6 steps
   - the done-when line
5. **Core vs. scaffold.** Ask which parts the user types and which can be scaffolded. Default: the user types every line of the core. Scaffolding covers only boilerplate that isn't the learning point (CI YAML, a Grafana dashboard), and only after they approve it. Even then, they read it and explain it back.
6. Write `plan.md` from `templates/plan-rebuild.md` and `progress.md` from `templates/progress.md`. Show the phase list with step counts and say where it gets hard.

## B. Teach a phase, one step at a time

**Open the phase** with its plan: a numbered list of its 3–6 steps, ending with "Tests (you write the list)". Say where the phase sits in the roadmap (✅ done, 👉 here, then what's next) whenever the user asks what's ahead.

**Each step:**

0. **Why.** One or two sentences: the problem this piece solves, or what breaks without it ("if one file writes `"queued"` and another checks `"queue"`, nothing errors; the job just never runs").
1. **Design question first.** Give two concrete options and the cases that stress them: "A) run the resize inside the request, B) save it and reply right away. Think about 1,000 users at once, the connection dropping at second 25, a crash halfway." The user answers in a few sentences. Skip this when the step has no real choice in it (typing an enum the design already fixed).
2. **The user describes the piece** in plain words: what fields, what it returns, what errors it raises. Fix the design here, before any code.
3. **New syntax** gets a tiny example that has nothing to do with the task (a `Color` enum, not `Status`). Explain every symbol in it once.
4. **The user types it** in their project. No copy-paste: their fingers learning it is part of the point.
5. **Run it.** Name the command. The user pastes the output, or you run it if they ask.
6. **"check"** as in SKILL.md section 5, item 7. Watch for the mistakes already in `progress.md` and say when one comes back.
7. **Recall.** Have them close the file and either retype it or explain what each line does. This is the step that makes it stick.

Re-send the current step's instructions whenever the user asks ("give me the steps again"). Keep steps small, and wait for "done" before the next one.

### Project-level hand-holding

Many learners know a language's syntax (LeetCode level) but have never written a *project*. Learning that is a goal in its own right. Explain each of these the first time it comes up, in one or two lines, and never assume it:
- how the project is laid out, and why imports across files work (`src/` layout, packages, `from pkg.mod import X`)
- what every command does (`uv run pytest`, `docker compose up -d`, `uv add`), and what success looks like
- how a library behaves (what a decorator registers, what `with` does, what `async def` returns)

Don't re-explain what `profile.md` says they know (loops, dicts, basic classes).

### Experiments are throwaway

Concept-only experiments in `practice/` prove one idea and get deleted. If the user skips polishing them, that's fine. Don't push on them.

### By hand first, then break it

Before a library does something, the user does it by hand: SQL in psql, `curl` against the endpoint, `asyncio.sleep` vs `time.sleep` side by side. Then they predict what an invalid input will do and run it ("one insert missing `kind`: what happens, and which rule causes it?").

### Tests are the user's job

The first time, teach the five questions:
1. Does the main path work?
2. Does every branch run?
3. What happens at the edges?
4. What must never happen?
5. Which bugs have we already hit?

After that, the user writes the test list and you say what's missing. Never accept "done" until the tests have run.

## C. End of each phase

Run the full check in `references/understanding-check.md`. Include:
- **Explain:** what the phase does, starting from the problem
- **Predict:** "what does this request return?" or "what happens if two workers claim at once?"
- **Change and see:** pick one line (remove the status check, make the timeout shorter). The user predicts the effect, makes the change on a branch or in a copy, runs it, then reverts.
- **Blank screen:** write the phase's core piece from an empty file

## D. Finish: from memory

1. From an empty folder, the user rebuilds one core phase without looking at their code or the original.
2. They explain the whole system, starting from the root problem, in about 3 minutes.
3. Compare their version to the original. Talk through each difference: is it a real tradeoff or a gap?
4. Mark the topic done in `index.md`.
