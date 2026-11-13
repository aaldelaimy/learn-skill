# Intake

Runs once per topic, before any plan. The goal is a plan that fits this learner: it skips what they know and uses what they know as a bridge.

## 1. Collect what's already known (don't ask what you can find)

Look, in this order:
- `~/learning/<slug>/profile.md` (if it exists, intake is done; just check it is current)
- other topics in `~/learning/` (read-only): their `profile.md` for background, and their `progress.md` for what was **passed** (`[x]` with a check recorded). Background carries over. Progress does not: it becomes review items here (SKILL.md section 1).
- study material made before this skill, read-only: `find ~ -maxdepth 5 \( -iname 'ROADMAP.md' -o -iname 'study-plan*' -o -name '.rederive' \) -not -path '*/Library/*' -not -path '*/node_modules/*'`. A progress tracker shows what the user has actually finished, e.g. "C through structs; malloc in progress". Use it as background only. Never edit it, and never take over its lessons.
- the user's resume or profile file if one exists (ask where it lives if a JD is the input), and the resume the goal is tied to
- the input itself: the JD, the syllabus, the repo's README and languages
- the user's own code, to judge their real level. A repo's code says more than a skills list (e.g. "LeetCode-level Python: loops, dicts, basic classes; never packaged a project").
- memory files Claude Code has loaded for this conversation

Note any claim the user may not be able to defend. For example, a resume lists C projects, but their other code shows no C. Raise it later in the plan, not as an accusation.

## 2. Ask only about the gaps

One message, at most 5 questions, numbered so they can answer "1. … 2. …". Typical gaps:

1. **Bridge:** what do you already know that's close to this? (a language, a course, a project)
2. **Goal and time:** interview, job, exam, or building something? Is there a date? Hours per week?
3. **Depth:** understand the ideas, interview-ready, or production-ready?
4. **Scope:** for a JD, which requirements matter most to you? For school, which lectures or topics are on the exam? Anything to cut?
5. **Rebuild only:** which language and stack? Which parts do you want to type yourself, and which can be scaffolded?

If they say "just go", or everything is already clear, skip the questions. List the assumptions at the top of `plan.md` under "Assumed" and continue.

## 3. Record it

Fill the "Learned in other topics" section of `profile.md` as a dated snapshot. Write one line per passed item: what it is, which topic or tracker it came from (slug or path), and when it was passed. Leave out anything in progress. This snapshot is the only trace another topic leaves in this one.


Write `profile.md` from `templates/profile.md`. Update it whenever the user mentions new background ("I took an OS class", "I've never used Docker"). Never ask a question `profile.md` already answers.

## 4. Use it visibly

The plan must show the profile at work:
- **Skipping:** "loops, functions, dicts: you know these from Python"
- **Bridges:** "threading.Lock → mutex: same idea, one level lower"
- **Honesty flags:** "your resume lists X; Phase N gets you able to defend it"
