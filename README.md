# Hang Math

Picture hanging arithmetic. A picture 18 tall centered 57 from the floor, with the wire 3 below the top, needs its nail at 63, not 57.

## What it computes

All measurements are numbers up to 9999.99 with at most 2 decimals, in one unit of your choice.

- **The nail truth** - the nail height from the floor for a picture's height, center height and wire drop (wire pulled taut), plus the top and bottom edge heights.
- **The row truth** - 1 to 20 pictures of one width on a wall with equal gaps including both ends, with every left edge from the left end of the wall, or how much wall is missing.
- **The mat truth** - the border a centered picture leaves inside a mat opening, or how far it is too wide or too tall.

## Boundary

Arithmetic only. It works out nail heights, spacing and borders from the owner's own measurements. It does not know the wall, studs, anchors or hooks, or what a hook can hold, and gives no verdict on whether any picture is safe to hang or looks right.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt hundredths, half-up rounding).
- `oracle.py` - the Python mirror (Fractions and Decimal, edges placed one picture at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (168 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/hangmath/
Repo: https://github.com/iLanis-agent/hangmath
