"""코스 5(물리Ⅱ) 빌더 공통: 복습 출처 태그와 챕터 기록."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sk import ex, eg, num, fb, order, wr, write_chapter

G = "(중력 가속도 g = 10 m/s²)"


def graph(xl, yl, xr, yr, curves, points=None, xs=1, ys=1):
    return {"widget": "graph", "static": True, "config": {
        "xlabel": xl, "ylabel": yl, "xmin": xr[0], "xmax": xr[1], "ymin": yr[0], "ymax": yr[1],
        "xstep": xs, "ystep": ys, "curves": curves, "points": points or []}}


def line(c0, c1, a, b):
    return {"kind": "poly", "coef": [c0, c1], "from": a, "to": b}


def run(no, title, lessons, review, srcs):
    assert len(review) == len(srcs)
    for q, s in zip(review, srcs):
        q["source_lesson"] = f"c5-ch{no:02d}-l{s:02d}"
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "content")
    write_chapter(root, 5, "물리Ⅱ", no, title, lessons, review, curriculum="2022-high")
