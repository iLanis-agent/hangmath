#!/usr/bin/env python3
# Hang Math oracle - mirrors engine.js with Fractions and Decimal rounding; edges are placed one picture at a time.
import json, re, random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

COUNT_ERR = "the number of pictures must be a whole number from 1 to 20"

def dec(t, name, zero_ok=False):
    t = t.strip() if isinstance(t, str) else ""
    m = re.fullmatch(r"([0-9]{1,4})(?:\.([0-9]{1,2}))?", t)
    err = f"the {name} must be a number {'from 0' if zero_ok else 'above 0'} and up to 9999.99, with at most 2 decimals"
    if not m: raise ValueError(err)
    v = Fraction(int(m.group(1))) + Fraction(int((m.group(2) or "0").ljust(2, "0")), 100)
    if v == 0 and not zero_ok: raise ValueError(err)
    return v
def fmt(fr):
    d = (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    if "." in s: s = s.rstrip("0").rstrip(".")
    if s == "-0": s = "0"
    return s
def plural(n, one, many): return f"{n} {one if str(n) == '1' else many}"

def hang(height, center, drop):
    h = dec(height, "picture height"); c = dec(center, "center height"); d = dec(drop, "wire drop", True)
    if d > h: raise ValueError("the wire drop must be from 0 up to the picture height")
    if c < h / 2: raise ValueError("the bottom of the picture would be below the floor")
    top = c + h / 2; bot = c - h / 2
    nail = top - d
    return f"A picture {fmt(h)} tall with its center {fmt(c)} from the floor and the wire {fmt(d)} below the top edge when pulled taut: put the nail {fmt(nail)} from the floor. The top edge sits at {fmt(top)} and the bottom edge at {fmt(bot)}."

def row(wall, count, pic):
    W = dec(wall, "wall width"); p = dec(pic, "picture width")
    t = count.strip() if isinstance(count, str) else ""
    if not re.fullmatch(r"[0-9]{1,2}", t) or not 1 <= int(t) <= 20: raise ValueError(COUNT_ERR)
    n = int(t)
    pics = plural(n, "picture", "pictures")
    if n * p > W:
        return f"{pics} {fmt(p)} wide need {fmt(n*p)} of wall, which is {fmt(n*p-W)} more than the {fmt(W)} you have."
    g = (W - n * p) / (n + 1)
    x = g; edges = []
    for _ in range(n):
        edges.append(fmt(x)); x += p + g
    return f"{pics} {fmt(p)} wide on a wall {fmt(W)} wide leave {fmt(g)} {'on each side' if n == 1 else 'at each end and between pictures'}. {'Left edge at ' if n == 1 else 'Left edges at '}{', '.join(edges)}."

def mat(ow, oh, pw, ph):
    ow = dec(ow, "opening width"); oh = dec(oh, "opening height"); pw = dec(pw, "picture width"); ph = dec(ph, "picture height")
    head = f"Opening {fmt(ow)} by {fmt(oh)} and picture {fmt(pw)} by {fmt(ph)}: "
    if pw > ow or ph > oh:
        parts = []
        if pw > ow: parts.append(f"{fmt(pw-ow)} too wide")
        if ph > oh: parts.append(f"{fmt(ph-oh)} too tall")
        return head + "the picture does not fit, " + " and ".join(parts) + "."
    s = (ow - pw) / 2; t = (oh - ph) / 2
    if s == t: return head + f"the border is {fmt(s)} all round."
    return head + f"the borders are {fmt(s)} on each side and {fmt(t)} at the top and bottom."

FNS = {"hangTruth": hang, "rowTruth": row, "matTruth": mat}

def cases():
    c = []
    rnd = random.Random(696)
    for a in [["18","57","3"],["18","57","0"],["18","57","18"],["18","9","3"],["18","8.99","3"],["18","57","18.01"],["0.01","0.01","0"],["9999.99","9999.99","9999.99"],["24.5","57.25","2.75"],["0","57","3"],["18","0","3"],["18","57","-1"],["18","57",""],["x","57","3"],["18.123","57","3"],["10000","57","3"],[" 18 "," 57 "," 3 "],["18.","57","3"],["1","0.5","0.5"],["7.77","33.33","1.11"]]:
        c.append(("hangTruth", a))
    for _ in range(35):
        h = rnd.randint(1, 5000) / 100
        cc = rnd.randint(1, 20000) / 100
        d = rnd.randint(0, int(h * 100)) / 100
        c.append(("hangTruth", [f"{h:.2f}", f"{cc:.2f}", f"{d:.2f}"]))
    for a in [["100","3","20"],["100","1","20"],["100","5","20"],["100","5","25"],["100","5","20.01"],["100","20","1"],["100","20","5"],["100","21","5"],["100","3","0.33"],["10","3","3"],["10","3","3.33"],["9999.99","20","0.01"],
              ["100","0","20"],["100","21","20"],["100","3","0"],["0","3","20"],["100","x","20"],["100","","20"],[" 100 "," 3 "," 20 "],["100","03","20"],["100","2.5","20"],["99.99","7","11.11"],["1","1","1"],["1","1","1.01"]]:
        c.append(("rowTruth", a))
    for _ in range(35):
        W = rnd.randint(100, 30000) / 100; n = rnd.randint(1, 20); p = rnd.randint(1, int(W * 100 / n) + 200) / 100
        c.append(("rowTruth", [f"{W:.2f}", str(n), f"{p:.2f}"]))
    for a in [["16","20","11","14"],["16","20","12","16"],["16","20","16","20"],["16","20","17","20"],["16","20","16","21"],["16","20","17","21"],["16","20","15.99","19.99"],["16","20","15.5","20"],["8","10","5","7"],["0.01","0.01","0.01","0.01"],
              ["0","20","11","14"],["16","0","11","14"],["16","20","0","14"],["16","20","11","0"],["x","20","11","14"],["16","20","11",""],[" 16 "," 20 "," 11 "," 14 "],["16","20","11.001","14"],["16.5","20.25","11.75","14.5"]]:
        c.append(("matTruth", a))
    for _ in range(35):
        ow = rnd.randint(100, 5000) / 100; oh = rnd.randint(100, 5000) / 100
        pw = rnd.randint(50, int(ow * 100) + 100) / 100; ph = rnd.randint(50, int(oh * 100) + 100) / 100
        c.append(("matTruth", [f"{ow:.2f}", f"{oh:.2f}", f"{pw:.2f}", f"{ph:.2f}"]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
