"""코스별 course.json 생성.

각 코스 폴더의 ch*/chapter.json을 읽어 content/level1/{코스}/course.json을 만든다.
코스 제목과 설명은 content/level1/courses.json에서 가져온다.
레슨을 다시 만든 뒤에는 이 스크립트도 다시 실행한다.

사용: python3 make_course_index.py [content 경로 ...]
"""
import json, os, sys, glob


def build(root):
    l1 = os.path.join(root, "level1")
    courses = json.load(open(os.path.join(l1, "courses.json"), encoding="utf-8"))["courses"]
    made = []
    for c in courses:
        cdir = os.path.join(l1, c["id"])
        chs = sorted(glob.glob(os.path.join(cdir, "ch*", "chapter.json")))
        if not chs:
            continue
        chapters, tl, tq, tr = [], 0, 0, 0
        for p in chs:
            d = json.load(open(p, encoding="utf-8"))
            lq = sum(l["questions"] for l in d["lessons"])
            rq = d["review"]["questions"] if d.get("review") else 0
            chapters.append({"no": d["chapter"]["no"], "id": d["chapter"]["id"], "title": d["chapter"]["title"],
                             "dir": os.path.basename(os.path.dirname(p)), "lessons": len(d["lessons"]),
                             "lesson_questions": lq, "review_questions": rq})
            tl += len(d["lessons"]); tq += lq; tr += rq
        out = {"schema_version": "1.0", "level": 1,
               "course": {"id": c["id"], "title": c["title"], "description": c["description"]},
               "totals": {"chapters": len(chapters), "lessons": tl, "lesson_questions": tq,
                          "review_questions": tr, "questions": tq + tr},
               "chapters": chapters}
        json.dump(out, open(os.path.join(cdir, "course.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        made.append(f"{c['id']}: 챕터 {len(chapters)}, 레슨 {tl}, 문항 {tq + tr}")
    return made


if __name__ == "__main__":
    roots = sys.argv[1:] or ["/home/claude/math-arena/content", "/home/claude/site/content"]
    for r in roots:
        print(r)
        for line in build(r):
            print("  " + line)
