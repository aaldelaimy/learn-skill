# Understanding check

The point is to catch fake understanding before moving on. This copies the session where the user asked "how can I know I didn't fake understand pointers and structs?": an honest read of the evidence, three kinds of tests, a pass bar stated up front, then targeted follow-up sets until it is real.

## What fake understanding looks like

- They can fix code once you point at the problem, but can't start from a blank screen.
- They can't predict what code will do before running it.
- They change symbols until the compiler or the tests pass: the same wrong type survives several rounds even after the error names the right one.
- They answer with a term ("make it atomic", "use a mutex") but can't say how it works or what it prevents.
- An answer is right for one input only. Test a second one.
- They say "got it" right after an explanation, with nothing new produced.

When you see any of these, run a check before moving on, even mid-lesson.

## When

- **Small**, after each lesson or rederive decision: 2–3 predict-or-explain questions.
- **Full**, every 2–3 lessons, at each phase end, and whenever the user asks "do I really get this?"
- **Phase end** adds a blank-screen build of the phase's core piece. Examples: a linked list that passes `-fsanitize=address`, or the `Job` model from memory.

## Format of the full check

### 1. Honest read

Two short lists built from their actual work, with no flattery:
- **Real understanding:** things they came up with themselves, bugs they explained correctly, why-questions that showed they were reasoning
- **Not solid yet:** where it took many rounds, what survived several reviews, what they guessed

### 2. Three tests, with no notes, no AI, and no compiler for tests 1–2

**Test 1: Predict the output.** 2–3 new snippets that mix concepts from the stretch being checked, each with one trap (pass-by-copy, pointer arithmetic, a struct passed by value). They answer before running anything.

**Test 2: Explain it as if to an interviewer.** 2 why-questions ("what's the difference between `p = q;` and `*p = *q;`?", "why is `sizeof(arr)` 8 inside a function?"). Grade on whether the mechanism is there, not on the words used.

**Test 3: Blank screen,** 10–20 minutes, no looking back. A small task they haven't done in exactly this form. Add one thinking twist that ties it to an earlier contrast ("in `best_student` overwriting the box was wrong; here, is changing the boxes right or wrong? why?"). They say "check q6" when the file is written.

### 3. How to judge yourself

State the pass bar before they start: "If you get Q1–Q5 right and write Q6 without reaching for help, you understand X. Any misses show exactly what to review. Either result is useful."

## Grading and follow-up

- Mark each answer right or wrong, with the reason in one line. Never reveal answers before they've answered.
- For each miss: reteach that one point from a new angle (a drawing, a smaller example), then ask a **fresh** question on the same point. Never repeat the same question.
- If several misses share one idea, give a short follow-up set (Set 2, Set 3) on just that idea until they get it right.
- Add every miss to the review queue in `progress.md`.
- Mark the lesson, phase, or decision done only after a pass. Never tell them "you understand this" without evidence from this check.
