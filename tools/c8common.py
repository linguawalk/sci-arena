"""코스 8(지구과학Ⅱ) 빌더 공통."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sk import ex, eg, num, fb, order, wr, write_chapter
from c1common import graph, line



def run(no, title, lessons, review, srcs):
    assert len(review) == len(srcs)
    for q, s in zip(review, srcs):
        q["source_lesson"] = f"c8-ch{no:02d}-l{s:02d}"
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "content")
    write_chapter(root, 8, "지학Ⅱ", no, title, lessons, review, curriculum="2022-high")
