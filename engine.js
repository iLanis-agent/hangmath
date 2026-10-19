// Hang Math engine: nail height, even spacing on a wall and mat borders, exact in hundredths on BigInt. One unit of your choice.
var COUNT_ERR = "the number of pictures must be a whole number from 1 to 20";

function _dec(t, name, zeroOk) {
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]{1,2}))?$/.exec(t);
  var err = "the " + name + " must be a number " + (zeroOk ? "from 0" : "above 0") + " and up to 9999.99, with at most 2 decimals";
  if (!m) throw new Error(err);
  var v = BigInt(m[1]) * 100n + BigInt((m[2] || "").padEnd(2, "0"));
  if (v === 0n && !zeroOk) throw new Error(err);
  return v; // hundredths
}
// num/den (in hundredths) rounded half up to hundredths of the unit, shown with trailing zeros dropped
function _fmt(num, den) {
  var neg = num < 0n; if (neg) num = -num;
  var v = (2n * num + den) / (2n * den);
  var s = (v / 100n).toString(), f = (v % 100n).toString();
  if (f.length < 2) f = "0" + f;
  f = f.replace(/0+$/, "");
  return (neg && v !== 0n ? "-" : "") + (f ? s + "." + f : s);
}
function _plural(n, one, many) { return n + " " + (String(n) === "1" ? one : many); }

function hangTruth(height, center, drop) {
  var h = _dec(height, "picture height", false);
  var c = _dec(center, "center height", false);
  var d = _dec(drop, "wire drop", true);
  if (d > h) throw new Error("the wire drop must be from 0 up to the picture height");
  if (2n * c < h) throw new Error("the bottom of the picture would be below the floor");
  var top = 2n * c + h, bot = 2n * c - h, nail = 2n * c + h - 2n * d; // all x2 hundredths
  return "A picture " + _fmt(h, 1n) + " tall with its center " + _fmt(c, 1n) + " from the floor and the wire " + _fmt(d, 1n) + " below the top edge when pulled taut: put the nail " + _fmt(nail, 2n) + " from the floor. The top edge sits at " + _fmt(top, 2n) + " and the bottom edge at " + _fmt(bot, 2n) + ".";
}
function rowTruth(wall, count, pic) {
  var W = _dec(wall, "wall width", false);
  var p = _dec(pic, "picture width", false);
  var t = typeof count === "string" ? count.trim() : "";
  if (!/^[0-9]{1,2}$/.test(t) || parseInt(t, 10) < 1 || parseInt(t, 10) > 20) throw new Error(COUNT_ERR);
  var n = BigInt(parseInt(t, 10));
  var pics = _plural(Number(n), "picture", "pictures");
  var need = n * p;
  if (need > W) return pics + " " + _fmt(p, 1n) + " wide need " + _fmt(need, 1n) + " of wall, which is " + _fmt(need - W, 1n) + " more than the " + _fmt(W, 1n) + " you have.";
  var R = W - need;
  var edges = [];
  for (var i = 0n; i < n; i++) edges.push(_fmt((i + 1n) * R + i * p * (n + 1n), n + 1n));
  var gap = _fmt(R, n + 1n);
  return pics + " " + _fmt(p, 1n) + " wide on a wall " + _fmt(W, 1n) + " wide leave " + gap + (n === 1n ? " on each side" : " at each end and between pictures") + ". " + (n === 1n ? "Left edge at " : "Left edges at ") + edges.join(", ") + ".";
}
function matTruth(openW, openH, picW, picH) {
  var ow = _dec(openW, "opening width", false), oh = _dec(openH, "opening height", false);
  var pw = _dec(picW, "picture width", false), ph = _dec(picH, "picture height", false);
  var head = "Opening " + _fmt(ow, 1n) + " by " + _fmt(oh, 1n) + " and picture " + _fmt(pw, 1n) + " by " + _fmt(ph, 1n) + ": ";
  if (pw > ow || ph > oh) {
    var parts = [];
    if (pw > ow) parts.push(_fmt(pw - ow, 1n) + " too wide");
    if (ph > oh) parts.push(_fmt(ph - oh, 1n) + " too tall");
    return head + "the picture does not fit, " + parts.join(" and ") + ".";
  }
  var s = ow - pw, t = oh - ph;
  if (s === t) return head + "the border is " + _fmt(s, 2n) + " all round.";
  return head + "the borders are " + _fmt(s, 2n) + " on each side and " + _fmt(t, 2n) + " at the top and bottom.";
}
