# Rederive mode

The user learns a finished project by designing it themselves from the bare problem, one decision at a time. Each decision is then tied to the real code and proved by running it. The input is a local path or a git URL: the user's own project or anyone else's.

Two kinds of knowledge, handled differently:
- **Design decisions** (how to keep two workers off the same job) are derived. Pose the problem and let the user build the answer.
- **Facts** (Postgres has its own clock, `%` can return a negative in C, what a readiness probe is) can't be derived. State them in one line with a bridge, then hand the problem back. Never turn a fact into a guessing game. A fact or concept passed in another topic gets one quick check question instead of a re-teach.

## A. Set up

1. **Repo.** For a local path, read it in place and never edit it. For a URL, run `git clone --filter=blob:none <url> ~/learning/<slug>/source`.
2. **Sandbox.** Run `git clone --no-hardlinks <repo> ~/learning/<slug>/sandbox` (or `cp -R` if it isn't a git repo). All experiments run there.
3. **Own or not.** The project is the user's own when most commits match `git config user.email`, or when they say so. For their own project, also read any resume line that mentions it. Those claims get tested at the end.

## B. Open with the root problem (before the map exists)

- **Their own project:** "Why did you build this? What problem did you have before any of this code existed?" If they answer with a feature list, ask once what they were trying to get done.
- **Someone else's:** work it out from the README and the first commits, then pose it with no solution words: "We have this problem: … How would you solve it?"

While they answer, build the map: with a background subagent if one is available, otherwise yourself. Add no constraints until the map exists. Until then, let them make their design work for the root problem alone.

## C. Build the map (`plan.md`)

1. Run `python3 -I scripts/repo_summary.py <repo>` (the path is relative to this skill's folder). It prints notable commits, design docs, entry points, and the dependency graph. Read the README, the design docs, and the entry points, and follow the imports outward. Trust code and diffs over commit messages.
2. Pick 5–10 decisions: mechanisms the user could invent from the problem. Examples: how data moves, how state is stored, how failures are handled, why a part is separate and what crosses its boundary. Skip choosing a language or library for its known strengths, and skip naming, styling, and config.
3. Order them the way the system would be built from nothing. D1 is the first thing the root problem forces.
4. For each decision, fill in `templates/plan-rederive.md`: problem, given, constraints (each with the naive design it breaks), facts to tell, the decision's general name, options with tradeoffs, **where it lives in the code** (`file:line` ranges at the mapped commit), **a break-it experiment** (a command to run in `sandbox/` that shows the naive version failing; write "none" when it would need heavy infrastructure, and use a small standalone demo in `practice/` instead), and evidence.
5. Don't show the map to the user. It holds the answers. Never list the decisions ahead or say how many there are.

## D. Run a decision

Take the first decision not marked done in `progress.md`, unless the user picks another.

1. **Open.** State the problem and what is given in 2–4 sentences, as if the code didn't exist. Ask how they'd solve it.
2. **Add constraints one at a time.** "With <constraint>, your design does <specific failure>. How would you change it?" When the map has an experiment, let them **see** the failure: they run it in the sandbox and read the output ("48 of 50 workers claimed the same job").
3. **Facts.** When the next step needs a fact, state it plainly with a bridge ("Postgres is a program with its own clock, like `time.time()` but on the server every worker shares"), then go back to the problem.
4. **A better idea is a win.** If their design beats the original, say so. If a constraint in the map explains the original, bring it in next. If none does, say theirs is better and log it.
5. **Stuck.** Use the two-hint cap from SKILL.md section 5, item 7. Then lay out the options from the map with one-line tradeoffs and ask which fits. If they pick wrong, apply the constraint that breaks it. If they've seen the options and still ask for the answer, give it, then have them explain it back in their own words.
6. **Diagram on request.** After two wrong answers in a row, offer a quick sketch: the existing parts, what moves between them, and where the constraint breaks. Never draw the missing piece.
7. **Name it.** As soon as they reach it: "Yes, that's compare-and-set: the write only succeeds if the row still has the value you read." Use the general engineering name and one line of definition.
8. **Into the real code.** Ask: "Where in this repo do you think that lives, and what would the line look like?" Let them guess, then open the real lines together (`file:line`). Point out where their version differs from the code, if it matters.
9. **Predict, change, run.** Pick one line that carries the decision. The user predicts what happens if it changes (delete the `WHERE status = 'queued'`, shrink the lease to 1 s), makes the change in `sandbox/`, runs it, compares with their prediction, and reverts.
10. **Polish.** Push on their design ("what about two sweepers at once?") until it holds up. Then run the small understanding check for the decision and log it.

Keep messages short, with one question per message. Before sending, count the questions and keep only the first.

## E. Log each decision in `progress.md`

```
## D1. <title> [done | in progress]
struggled with: <where they got stuck, and what got them moving>
found on their own: <ideas reached without a hint>
did well: …
did ok: <worked, but shaky or needed help>
better idea: <only if they had one>
review: <1–2 questions for the review queue>
```

Watch the log for patterns across decisions (for example, naming a tool before reasoning about the problem). Mention a pattern once when you see it repeat, and turn it into review questions.

## F. Finish

1. **From memory:** the user explains the whole system from the root problem through every decision, with no notes and no code open.
2. **Grilling:** 5–8 interviewer-style "why not X?" questions across the decisions ("why not just use a mutex?", "why not poll the DB?"). Grade each answer.
3. **Resume claims** (their own project): for each resume line about it, they defend the claim and its number out loud. Flag any claim they can't back up.
4. Mark the topic done in `index.md`, and tell them where the log is (full path).

## Older `.rederive/` folders

If the repo has a `.rederive/log.md` from the older rederive skill, mention it once. Offer to import it as the starting log, and only do so if the user says yes. Never modify the old folder.
