# Teach mode

The input is a topic, a job description, or school material. The output is `plan.md` and `progress.md`, then one lesson at a time.

## A. Build the plan

### From a job description (pasted text or a file path)

1. Read the whole posting. Sort its lines into minimum qualifications, preferred qualifications, and duties. Drop boilerplate (EEO, pay, agencies).
2. Ask which ones to focus on if `profile.md` doesn't say. A new grad is usually tested on the qualifications more than the duties. Domain duties (e.g. wireless protocols) often shrink to one skim session.
3. For each qualification, write "what they'll likely test" and give it a share of the time. Weight = how heavily the JD stresses it × how far the profile is from it.
4. **Resume check.** If a resume for this role exists, list the claims the user can't defend yet. Add a "be ready to explain" table, one row per claim, naming the questions an interviewer would ask. Schedule a rederive of those projects once the basics are in place.
5. **Topics learned elsewhere** (from the "Learned in other topics" snapshot in `profile.md`) stay in the plan as review items. Mark them `[R]`, give each one a review check (2–3 questions asked from this goal's angle, e.g. `volatile` for registers rather than in general), and give each a fallback: "miss → full lesson here". Never drop them, and never point to the other topic for them.
6. **Phases** in prerequisite order, each with weeks or days estimated from hours per week. Keep a light practice track (e.g. one algorithm problem a day in the language they know) running alongside the new material, so neither gets rusty.
7. **Bridge table:** what changes from their known language or concept to the new one, and why each difference matters. At most about 8 rows.
8. Every topic gets a `[ ]` checkbox. Every phase ends with "Done with this phase when you can, without notes:" and 3–5 concrete abilities.
9. **"If time is short":** a priority table (rank, topic, why) so a sudden interview date doesn't break the plan.
10. **Final phase**, once there is a date: resume stories said out loud, behavioral questions, timed mock rounds, and asking the recruiter about format and allowed languages.
11. **Resources:** one main pick plus one reference. Not a list of ten.

### From school material (slides, PDFs, syllabus, homework, exam topic list)

1. Read every file. List each lecture's concepts. If a file can't be read, say which one.
2. Ask, or read from the syllabus, which lectures and topics the exam covers. Weight topics by exam scope and by how much homework touched them.
3. Follow the lecture order, but move a topic earlier when a later one depends on it. Tag each topic with its lecture number so the user can find the slides.
4. Exercises match what the exam will ask (derivations, traces, short code, calculations). Use homework and past exams as the model, never as answers to hand over.
5. Final phase: a timed practice exam made by you, graded, with misses sent back into the plan.

### From a bare topic ("teach me RTOS scheduling")

Ask the goal if intake didn't settle it. Break the topic into prerequisite-ordered concepts, skip what the profile covers, and write a done-when line for each.

### Write the files

- `plan.md` from `templates/plan-teach.md`
- `progress.md` from `templates/progress.md`: a lesson table (number, lesson, exercise, status) with a "You are here" line
- `practice/`: set up the toolchain on day 1 and show the exact build or run command (e.g. `clang -Wall -Wextra -g -fsanitize=address f.c -o f && ./f`)

Show the plan, then offer to start Lesson 1. Make a PDF only if the user asks for one.

## B. Run a lesson

The shape every lesson took:

1. **The problem.** Two or so things you can't do with what you know so far ("you can't choose an array's size while the program runs").
2. **The concept, bridged.** "Python does this for you with X. C makes you do it, which is why Y." Use a lookup table only for side-by-side differences. Draw a box-and-arrow picture for anything about memory or state.
3. **A demo file** in `practice/` (`<concept>_demo.ext`), split into numbered steps with comments. Run it and paste its real output, including a failure the user should recognize next time (sanitizer report, compiler error, exception).
4. **At most 3 rules,** each one line. These go into `notes.md` once the user has used them.
5. **The exercise** in `practice/exN.ext`, following `templates/exercise.md`: the user writes the functions, `main` already checks them, and the expected output sits at the bottom. Include one "find the bug, then explain why in a comment" part where it fits.
6. **"check" loop** as in SKILL.md section 5, item 7. When an error message is new, teach how to read it (which line is the what, which is the where).
7. **Side topics.** When the user asks something tangential, answer briefly and log it on the lesson's "side topics covered" row.
8. **Understanding check** (`references/understanding-check.md`), small after each lesson and full every 2–3 lessons and at each phase end.
9. **Update the files,** then say what's next in one line.

## Interview-depth topics

For each concept, add the question an interviewer would ask about it, and a one-line answer the user writes themselves in `notes.md`. Example: "Why is `sizeof(arr)` 8 inside a function?"
