"""sci-arena 레벨2·3 가이드 공용 도구 (math-arena·tech-arena 공통 단원 템플릿).

과목: overview(분야 개요), prereq(선수지식 점검 + 레벨1 연결), units(로드맵), next(다음 과목)
단원: objectives(학습 목표), checklist(핵심 개념), advice(학습 조언 1~2문단),
      resources(추천 자료), hours(예상 학습 시간), after(먼저 볼 단원), selfcheck(자가점검 문항)
자가점검 문항은 레벨1 문항 스키마를 그대로 써서 같은 채점 코드로 동작한다.
"""
import json, os

CONTENT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

TRACKS = [
    {"id": "physics", "title": "물리", "note": "미적분 기반 일반물리에서 시작해 역학·전자기학·양자역학으로 나아갑니다.",
     "l2": [["general-physics", "일반물리"]],
     "l3": [["classical-mechanics", "고전역학"], ["electromagnetism", "전자기학"], ["thermal-statistical", "열·통계물리"],
            ["waves-optics", "파동·광학"], ["quantum-mechanics", "양자역학"], ["modern-physics", "상대성이론과 현대물리"]]},
    {"id": "chemistry", "title": "화학", "note": "원자 구조와 결합에서 시작해 물리·유기·무기·분석화학의 네 기둥으로 나뉩니다.",
     "l2": [["general-chemistry", "일반화학"]],
     "l3": [["physical-chemistry", "물리화학"], ["organic-chemistry", "유기화학"], ["inorganic-chemistry", "무기화학"],
            ["analytical-chemistry", "분석화학"]]},
    {"id": "biology", "title": "생명과학", "note": "분자에서 생태계까지. 세포·분자와 유전학을 먼저 공부하면 나머지가 쉬워집니다.",
     "l2": [["general-biology", "일반생물"]],
     "l3": [["cell-molecular", "세포·분자생물학"], ["genetics", "유전학"], ["physiology", "생리학"],
            ["ecology-evolution", "생태학과 진화"], ["microbiology", "미생물학"]]},
    {"id": "earth", "title": "지구과학", "note": "고체 지구, 대기, 해양, 우주의 네 분야. 물리·화학 레벨2와 함께 공부하면 좋습니다.",
     "l2": [["earth-science", "지구과학개론"]],
     "l3": [["geology", "지질학"], ["atmospheric-science", "대기과학"], ["oceanography", "해양학"], ["astronomy", "천문학"]]},
    {"id": "convergence", "title": "융합", "note": "분과를 가로지르는 주제. 레벨2는 과학의 방법, 레벨3은 분과가 만나는 응용 분야입니다.",
     "l2": [["science-method", "과학사와 과학의 방법"]],
     "l3": [["biochemistry", "생화학"], ["environment-climate", "환경·기후과학"], ["materials-science", "재료과학"],
            ["biotechnology", "생명공학"], ["astrophysics", "천체물리"]]},
]
LEVELS = {"2": "대학 일반과학 (전문대졸·대학 1학년 수준)", "3": "전공 핵심 (대졸·학부 전공 수준)"}
VALIDATION = {"2": "대학 일반물리·일반화학·일반생물·지구과학개론 표준 교재의 목차",
              "3": "학부 전공필수 과목 구성과 중등교사 임용시험(물리·화학·생물·지구과학) 과목 구성"}

# 자주 쓰는 공개 자료
OPENSTAX = lambda title, slug: {"kind": "book", "provider": "OpenStax (무료 공개 교재)", "title": title,
                                "url": f"https://openstax.org/details/books/{slug}", "lang": "영어"}
KHAN = lambda title, path: {"kind": "video", "provider": "Khan Academy", "title": title,
                            "url": f"https://www.khanacademy.org/science/{path}", "lang": "영어(일부 한국어)"}


def R(base, part):
    d = dict(base); d["part"] = part; return d


def book(provider, title):
    return {"kind": "book", "provider": provider, "title": title}


def num(i, prompt, answer, expl, hint=None, fmt="integer", tol=0):
    q = {"type": "question", "id": f"q{i}", "qtype": "numeric", "prompt": prompt, "answer": str(answer),
         "answer_format": fmt, "tolerance": tol, "explanation": expl}
    if hint: q["hint"] = hint
    return q


def fill(i, prompt, blanks, expl, hint=None):
    q = {"type": "question", "id": f"q{i}", "qtype": "fill_blank", "prompt": prompt,
         "blanks": [{"id": k + 1, "answers": a if isinstance(a, list) else [a]} for k, a in enumerate(blanks)],
         "explanation": expl}
    if hint: q["hint"] = hint
    return q


def written(i, prompt, groups, need, model):
    return {"type": "question", "id": f"q{i}", "qtype": "written", "prompt": prompt,
            "rubric": {"visibility": "hidden", "keyword_groups": groups, "min_groups_matched": need},
            "model_answer": model}


def unit(no, title, hours, after, objectives, checklist, advice, resources, selfcheck):
    return {"no": no, "title": title, "hours": hours, "after": after, "objectives": objectives,
            "checklist": checklist, "advice": advice, "resources": resources, "selfcheck": selfcheck}


def check(subject, units):
    """최소 품질 검사"""
    nos = [u["no"] for u in units]
    assert nos == list(range(1, len(units) + 1)), "단원 번호"
    for u in units:
        where = f"{subject['id']} u{u['no']}"
        assert all(a < u["no"] for a in u["after"]), f"{where}: 선수 단원은 앞 단원이어야 함"
        assert len(u["objectives"]) >= 2 and len(u["checklist"]) >= 4, f"{where}: 목표·체크리스트"
        assert len(u["advice"]) >= 1 and all(len(a) >= 80 for a in u["advice"]), f"{where}: 조언 분량"
        assert u["resources"], f"{where}: 자료"
        assert 3 <= len(u["selfcheck"]) <= 6, f"{where}: 자가점검 3~6문항"
        for q in u["selfcheck"]:
            if q["qtype"] == "written":
                m = q["model_answer"]
                hit = sum(any(k in m for k in g) for g in q["rubric"]["keyword_groups"])
                assert hit >= q["rubric"]["min_groups_matched"], f"{where}: 모범 답안이 채점 기준 미달"
            else:
                assert len(q.get("explanation", "")) >= 10, f"{where}: 풀이"
            if q["qtype"] == "fill_blank":
                n = q["prompt"].count("{{")
                assert n == len(q["blanks"]), f"{where}: 빈칸 수"
    p = subject["prereq"]
    assert p["links"] and len(p["questions"]) >= 3, f"{subject['id']}: 선수 점검"


def write_subject(subject, units):
    check(subject, units)
    lv, tr, sid = subject["level"], subject["track"], subject["id"]
    base = os.path.join(CONTENT, f"level{lv}", tr, sid)
    os.makedirs(base, exist_ok=True)
    subj = dict(subject, schema_version="1.0", type="guide_subject")
    for k, q in enumerate(subj["prereq"]["questions"]):
        q["id"] = f"p{k + 1}"; q["stage"] = "prereq"
    subj["units"] = [{"no": u["no"], "title": u["title"], "hours": u["hours"], "after": u["after"],
                      "file": f"u{u['no']:02d}.json"} for u in units]
    subj["total_hours"] = sum(u["hours"] for u in units)
    json.dump(subj, open(os.path.join(base, "subject.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for u in units:
        d = dict(u, schema_version="1.0", type="guide_unit", level=lv, track=tr, subject=sid,
                 id=f"l{lv}-{tr}-{sid}-u{u['no']:02d}")
        for k, q in enumerate(d["selfcheck"]):
            q["id"] = f"q{k + 1}"; q["stage"] = "selfcheck"
        json.dump(d, open(os.path.join(base, f"u{u['no']:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_tracks()
    n = sum(len(u["selfcheck"]) for u in units)
    print(f"{subject['title']}: {len(units)}단원, 약 {subj['total_hours']}시간, 자가점검 {n}문항, 선수 점검 {len(p_(subject))}문항")
    return subj


def p_(subject):
    return subject["prereq"]["questions"]


def write_tracks():
    out = {"schema_version": "1.0", "levels": LEVELS, "validation": VALIDATION, "tracks": []}
    for t in TRACKS:
        subs = []
        for lv, key in ((2, "l2"), (3, "l3")):
            for sid, title in t[key]:
                ok = os.path.exists(os.path.join(CONTENT, f"level{lv}", t["id"], sid, "subject.json"))
                subs.append({"level": lv, "id": sid, "title": title, "available": ok})
        out["tracks"].append({"id": t["id"], "title": t["title"], "note": t["note"], "subjects": subs})
    json.dump(out, open(os.path.join(CONTENT, "guides.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
