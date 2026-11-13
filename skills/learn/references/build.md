# Build mode

The user builds a new project for the first time and writes the code themselves. They should end up able to explain the whole request-to-result lifecycle, every failure mode, and every tradeoff without looking. No original exists, so Claude drafts an outline the user approves, plus a hidden design map that stays private.

The point of the mode: the project must not be vibe-coded. If Claude writes the system and the user studies it afterwards, they end up with a project they can't defend. This mode never falls back to that, even when progress is slow.

## A. Intake: the project brief

Run `references/intake.md`, then fill these gaps (skip any `profile.md` already answers):

1. **Identity:** what the system does, in two sentences, from a user's point of view.
2. **What it must prove:** the skills it should show, tied to the target roles or JDs. Also: what the repo should communicate ("understands how backend systems behave after the code is written"), and what it must not ("added Redis and Terraform because the JDs mention them").
3. **Stack:** the language and core tools. For each heavy piece (a cloud, IaC, a broker, Kubernetes), ask whether the goal really needs it and whether it costs money. Default to leaving it out until a problem requires it.
4. **Done means:** a checklist of observable facts ("jobs survive a worker crash", "load test numbers recorded"), ending with "I can explain the lifecycle and failure modes without the code".
5. **Time:** hours per week and any deadline. This sets the cut line.

## B. Draft two files

**`plan.md`, the outline the user approves.** Use `templates/plan-build.md`:
- the brief from A, plus an **avoid list** (things not to build unless everything else is done) and a **postpone list** (things to add only once a phase needs them)
- **phases named by the problem, never by the solution.** Write "Two workers must never run the same job", not "Atomic claim with UPDATE … WHERE". Write "Jobs must survive a restart", not "PostgreSQL". Tools may appear in the stack line, but a phase never says which mechanism solves it.
- each phase gets: the problem, what's given, the rough size, and its done-when (a behavior, not an implementation)
- **Phase 0 is project setup:** folders, the package or module file, the dependency tool, and one passing test the user writes, so the project structure is understood before any feature
- the simplest working version comes next: an in-memory, single-process version that runs end to end
- **concept-only phases** before any phase that needs a new runtime model (concurrency, async)
- a **measure** phase, a **break-it** phase, docs, and resume and interview phases near the end
- an estimate in weeks, and a **cut line**: "resume-ready after Phase N; the rest is optional"

**`design-map.md`, hidden from the user.** It uses the fields from `templates/plan-rederive.md`, with "In the code" replaced by "How to check it" (a test or experiment that proves it works). It holds each phase's real design questions, the constraints in order, the options, and the standard answer. Claude uses it to order the phases and to draft each step's design question (options and stress cases), the way rebuild uses the original repo. Never show it, and never say how many decisions it holds.

Show `plan.md` only. The user can reorder, cut, add, or change the stack. **Nothing starts until they accept it.** Record the acceptance date at the top. If they say "show me the design", show the relevant part of the map, and note in `progress.md` that they chose to see it.

## C. Teach each phase exactly like a rebuild

Build mode teaches the same way as rebuild mode. Run every phase with `references/rebuild.md`:
- **section B** for each step: the phase's step list, then why → design question → the user describes the piece → tiny unrelated syntax example → the user types it → run → "check" → recall. That includes project-level hand-holding, throwaway experiments, by hand first then break it, and the user writing the tests.
- **section C** at the end of each phase: the full understanding check

Move to the next phase only when the user says so.

There is one difference. In rebuild, the design question's options and stress cases come from reading the original repo. Here they come from `design-map.md`. Everything else about a step is identical:
- If the user's answer holds up against every stress case in the map, build their design even if it isn't the textbook one, and log it in `progress.md` as a better idea or an accepted tradeoff.
- If it breaks, apply the stress case that breaks it ("with 50 workers, what happens?"), and keep the two-hint cap.
- Debugging: name the bug, explain it, hint at the smallest fix. Never rewrite their code.

### Rules that hold the whole way

- **Every component has a reason.** A new service, library, or piece of infrastructure enters only when a problem in the current phase needs it, and the user can say which problem.
- **Don't skip ahead.** If the user wants something on the avoid or postpone list, say which phase would need it, and add it now only if they insist.
- **Minimal code.** Standard library where reasonable, no abstractions without a second user. If something isn't needed yet, say so and postpone it.
- **Never make up numbers or incidents.** Every number comes from a run logged in `progress.md`: date, command, environment, result. A postmortem must be about a problem that actually happened during the build. "Production-ready" is never claimed unless the plan defines what it means.
- **Keep application and infrastructure separate.** The app has to work and be tested before any deployment phase starts.
- **Scaffolding** (CI YAML, dashboard JSON, k6 boilerplate) only with the user's approval of that specific file. They read it and explain it back.

## D. Measure, break, document

- **Measure:** load tests the user writes and runs. Record p50, p95, p99, throughput, error rate, and queue depth in the measurement log. Optimize only a bottleneck that was measured, then measure again.
- **Break it:** planned failure experiments (crash a worker, restart a dependency, send a bad payload, deliver twice). The user predicts each outcome first, then runs it and writes down what happened.
- **Docs in the repo**, written by the user in a public-facing voice: README, `docs/design.md`, and `docs/postmortems/` (real incidents only). **No study material in the repo:** interview prep, notes, and resume bullets stay in `~/learning/<slug>/`.

## E. Finish

1. **Resume bullets,** drafted from the measurement log and the implemented features only. Every number links to its log entry.
2. **Interview prep:** the question list from the brief. The user answers each one out loud and gets graded, then gets grilled with "why not X?" across the decisions.
3. **From memory:** explain the lifecycle and the failure modes with no code open, then rebuild one core phase from an empty folder.
4. **Compare with real systems** (for a job queue: Celery, Sidekiq). For each difference, decide whether it's a tradeoff the user chose or a gap they can name.
5. Mark the topic done in `index.md`.
