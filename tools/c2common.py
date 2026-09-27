"""코스 2(화학Ⅰ) 빌더 공통."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sk import ex, eg, num, fb, order, wr, write_chapter
from c1common import graph, line

STP = "(0 °C, 1 atm에서 기체 1 mol의 부피는 22.4 L)"
NA = "(아보가드로수 6 × 10²³)"


def run(no, title, lessons, review, srcs):
    assert len(review) == len(srcs)
    for q, s in zip(review, srcs):
        q["source_lesson"] = f"c2-ch{no:02d}-l{s:02d}"
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "content")
    write_chapter(root, 2, "화학Ⅰ", no, title, lessons, review, curriculum="2022-high")
