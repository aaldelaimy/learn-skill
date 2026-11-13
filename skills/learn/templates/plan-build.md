# Build: <project name>

Your code: <folder> · drafted <YYYY-MM-DD> · **accepted by you: <YYYY-MM-DD, or "not yet">**
Design answers are kept in design-map.md and stay hidden. You'll work each one out when you reach its phase.

## Project brief
- **What it is:** <two sentences, from a user's point of view>
- **What it must prove:** <skills, tied to target roles or JDs>
- **The repo should say:** "<…>" · **It must not say:** "<…>"
- **Stack:** <language, core tools> · **Left out until a problem needs it:** <cloud, IaC, broker, …>
- **Time:** <hours per week> · about <N> weeks to the cut line

## Avoid (only if everything else is done)
- <e.g. Kubernetes, Kafka, auth, a frontend dashboard, multi-region>

## Postpone (until a phase needs it)
- <e.g. caching, tracing, deployment>

## Phases (each one is a problem; you design the solution when you get there)

### Phase 0: Project setup
- Folders, package/module file, dependency tool, one passing test you write · Done when: you can explain why your imports work and what each command does

### Phase 1: <the simplest end-to-end version, e.g. "Accept work and report on it, in one process">
- Problem: <what must work, with no solution terms>
- Given: <what exists>
- Size: ~<N> steps · Done when: <observable behavior>

### Phase 2: Concept only: <e.g. doing work while the request returns>
- Experiments in practice/, deleted afterwards

### Phase 3: <e.g. "Work must survive a restart">
…

### Phase N: Measure it
- Done when: p50/p95/p99, throughput, and error rate are recorded from real runs

### Phase N+1: Break it on purpose
- Planned failures: <crash, restart, bad input, duplicate delivery> · predict each one, run it, write down what happened

### Phase N+2: Docs (README, design.md, real postmortems)

**── cut line: resume-ready here ──**

### Optional phases
- <deployment, IaC, dashboards: each with the problem it would solve>

## Done means
- [ ] <observable fact>
- [ ] I can explain the full lifecycle and every failure mode without the code
- [ ] Every number on the resume links to a run in the measurement log

## Questions you'll answer at the end
- <Why X instead of the simpler Y? What happens if Z dies? Can a job run twice? …>
