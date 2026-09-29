"""진입 진단(배치 고사) 빌드 — sci-arena.

과학은 수학처럼 한 줄로 이어지지 않고 가지를 친다.
  c0 기초 과학 → 물리(c1 → c5), 화학(c2 → c6), 생명(c3 → c7), 지구(c4 → c8)
그래서 진단도 '기초 1개 + 과목 트랙 4개' 구조로 판정한다.

1) content/level1/placement.json: 챕터마다 진단에 쓸 문항 풀
   - 출처: 각 챕터의 review.json (복습 세트)
   - 제외: 서술형, 앞 문항에 기대는 문항("위 문제에서…", "같은 X에서…"),
           그림 없이 그림·그래프를 언급하는 문항
   - 실제 출제는 앞의 3문항 가운데 무작위 1문항
2) placement.html: player.html의 공용 구간을 placement_tpl.html에 끼워 넣어 생성.
   플레이어를 고치면 이 스크립트만 다시 실행.

사용: python3 tools/make_placement.py [사이트 경로]
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
L1 = os.path.join(SITE, "content", "level1")

BASE = "c0"
TRACKS = [
    {"id": "phys", "name": "물리", "a": "c1", "b": "c5"},
    {"id": "chem", "name": "화학", "a": "c2", "b": "c6"},
    {"id": "bio", "name": "생명과학", "a": "c3", "b": "c7"},
    {"id": "earth", "name": "지구과학", "a": "c4", "b": "c8"},
]
PER_CHAPTER = 5
PICK_FROM = 3
DEP = re.compile(r"^(같은|그 |그때|이때|위 |앞|이 )|(위|앞) (문제|반응|회로|궤도|용액|혼합|집단|진자|전지|변압기|실험|막대|코일|용수철|천체|행성|별|은하|식|과정|경우)|같은 (조건|경우|상황|운동|궤도|용기|온도|위도|장소|곡선|반응)")
FIGREF = re.compile(r"그림|그래프|도표")


def usable(q):
    if q.get("qtype") == "written":
        return False
    p = q.get("prompt", "")
    if DEP.search(p):
        return False
    if FIGREF.search(p) and not q.get("figure") and q.get("qtype") != "diagram":
        return False
    return True


def build_pool():
    courses = json.load(open(os.path.join(L1, "courses.json"), encoding="utf-8"))["courses"]
    ids = [BASE] + [t["a"] for t in TRACKS] + [t["b"] for t in TRACKS]
    meta = {c["id"]: c for c in courses}
    out = {"schema_version": "1.0", "level": 1, "base": BASE, "tracks": TRACKS,
           "pass_rate": 0.7, "pick_from": PICK_FROM, "courses": []}
    total = 0
    for cid in ids:
        c = meta[cid]
        if not c.get("available"):
            raise SystemExit(f"공개되지 않은 코스: {cid}")
        cj = json.load(open(os.path.join(L1, cid, "course.json"), encoding="utf-8"))
        chs = []
        for chm in cj["chapters"]:
            d = os.path.join(L1, cid, chm["dir"])
            rv = json.load(open(os.path.join(d, "review.json"), encoding="utf-8"))
            qs = [q for q in rv["questions"] if usable(q)]
            # 출제 후보(앞 3문항)가 서로 다른 레슨에서 오도록 레슨별로 번갈아 뽑는다
            groups = {}
            for q in qs:
                groups.setdefault(q.get("source_lesson", ""), []).append(q)
            order = sorted(groups)
            spread = []
            while any(groups[k] for k in order) and len(spread) < PER_CHAPTER:
                for k in order:
                    if groups[k] and len(spread) < PER_CHAPTER:
                        spread.append(groups[k].pop(0))
            qs = spread
            if len(qs) < PICK_FROM:
                raise SystemExit(f"진단 문항 부족({len(qs)}): {cid} {chm['dir']}")
            chs.append({"no": chm["no"], "dir": chm["dir"], "id": chm["id"], "title": chm["title"],
                        "review_id": rv["review"]["id"],
                        "questions": [dict(q, stage="diagnostic") for q in qs]})
            total += len(qs)
        out["courses"].append({"id": cid, "title": c["title"], "description": c["description"],
                               "chapters": chs})
    path = os.path.join(L1, "placement.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return path, total, sum(len(c["chapters"]) for c in out["courses"])


def build_page():
    from kit import render
    player = open(os.path.join(SITE, "player.html"), encoding="utf-8").read()
    tpl = open(os.path.join(HERE, "placement_tpl.html"), encoding="utf-8").read()
    page = render(tpl, player)
    path = os.path.join(SITE, "placement.html")
    open(path, "w", encoding="utf-8").write(page)
    return path, len(page)


if __name__ == "__main__":
    p, n, chs = build_pool()
    print(f"문항 풀: {p} ({chs}개 챕터, {n}문항)")
    p, size = build_page()
    print(f"진단 페이지: {p} ({size:,}바이트)")
