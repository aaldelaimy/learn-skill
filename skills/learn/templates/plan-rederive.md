# Decision map (hidden from the user: it holds the answers)

repo: <name> · built from: <short sha> · date: <YYYY-MM-DD> · sandbox: ~/learning/<slug>/sandbox
root problem: <in the user's words once they've said it>

## D1. <the problem, without naming the solution>
- Problem: <what has to work, no solution terms>
- Given: <what exists at this point>
- Constraints, in order:
  1. <constraint> -> breaks: <the naive design it rules out>
- Facts to tell (not derive): <platform facts the next step needs, each with a bridge>
- Decision: <general technique name> — <one-line definition> — <what the code does with it>
- Options: <2–4 approaches incl. the real one, one-line tradeoff each>
- In the code: <file:line-range> — <what those lines do>
- Experiment: <command run in sandbox/ that shows the naive version failing, and the expected output> | none (<why>; demo in practice/ instead)
- Change-and-run: <one line to change, and what the user should predict>
- Evidence: <commit sha "message", files, or "code only">
