"""sci-arena 레슨 빌더 공용 도구.

math-arena 레슨 스키마 v1.0을 그대로 따른다. 각 build_c{코스}_ch{NN}.py는
LESSONS·REVIEW 데이터를 만들고 write_chapter()를 호출한다.
엄격 검사(strict, 단계 A 기준): 채점형 문항 풀이 20자 이상, 적용·복습 문항 힌트 필수,
레슨당 예제 3개, 문항 15~17개, 화면 20~24개.
"""
import json, os

SITE = "sci-arena"


def ex(i, stage, title, *body, figure=None):
    d = {"type": "explain", "id": i, "stage": stage, "title": title, "body": list(body)}
    if figure: d["figure"] = figure
    return d


def eg(i, stage, problem, steps, answer, title="예제", figure=None):
    d = {"type": "example", "id": i, "stage": stage, "title": title, "problem": problem, "steps": steps, "answer": answer}
    if figure: d["figure"] = figure
    return d


def num(i, stage, prompt, answer, expl, hint=None, fmt="integer", tol=0, figure=None):
    d = {"type": "question", "id": i, "stage": stage, "qtype": "numeric", "prompt": prompt, "answer": str(answer),
         "answer_format": fmt, "tolerance": tol, "hint": hint, "explanation": expl}
    if figure: d["figure"] = figure
    return d


def fb(i, stage, prompt, answers, expl, hint=None, groups=None, figure=None):
    """answers: 빈칸마다 허용 답 목록(문자열 하나면 그 답만)."""
    blanks = [{"id": k + 1, "answers": [a] if isinstance(a, str) else list(a)} for k, a in enumerate(answers)]
    d = {"type": "question", "id": i, "stage": stage, "qtype": "fill_blank", "prompt": prompt, "blanks": blanks,
         "hint": hint, "explanation": expl}
    if groups: d["unordered_groups"] = groups
    if figure: d["figure"] = figure
    return d


def order(i, stage, prompt, correct, disp, expl, hint=None):
    """correct: 정답 순서의 문장 목록, disp: 화면 표시 순서(correct의 인덱스)."""
    ids = "abcdefgh"
    items = [{"id": ids[k], "text": correct[j]} for k, j in enumerate(disp)]
    ans = [ids[disp.index(j)] for j in range(len(correct))]
    return {"type": "question", "id": i, "stage": stage, "qtype": "ordering", "prompt": prompt, "items": items,
            "answer_order": ans, "hint": hint, "explanation": expl}


def wr(i, stage, prompt, groups, model, hint=None, need=2):
    return {"type": "question", "id": i, "stage": stage, "qtype": "written", "prompt": prompt, "hint": hint,
            "rubric": {"visibility": "hidden", "keyword_groups": groups, "min_groups_matched": need},
            "model_answer": model}


def check_lesson(lid, screens):
    qs = [s for s in screens if s["type"] == "question"]
    egs = [s for s in screens if s["type"] == "example"]
    errs = []
    if not 15 <= len(qs) <= 17: errs.append(f"문항 {len(qs)}개")
    if not 20 <= len(screens) <= 24: errs.append(f"화면 {len(screens)}개")
    if len(egs) != 3: errs.append(f"예제 {len(egs)}개")
    seen = set()
    for s in screens:
        if s["id"] in seen: errs.append(f"id 중복 {s['id']}")
        seen.add(s["id"])
        if s["type"] == "question":
            errs += check_q(s, need_hint=s["stage"] in ("apply", "review"))
    if errs: raise SystemExit(f"{lid}: " + ", ".join(errs))


def check_q(s, need_hint):
    e = []
    if s["qtype"] != "written" and len(s.get("explanation") or "") < 20: e.append(f"{s['id']} 풀이 짧음")
    if need_hint and not s.get("hint"): e.append(f"{s['id']} 힌트 없음")
    if s["qtype"] == "fill_blank" and s["prompt"].count("{{") != len(s["blanks"]): e.append(f"{s['id']} 빈칸 수")
    return e


def write_chapter(root, course, course_title, ch_no, ch_title, lessons, review, curriculum="2022-middle"):
    cdir = f"c{course}" if isinstance(course, int) else course
    d = os.path.join(root, "level1", cdir, f"ch{ch_no:02d}")
    os.makedirs(d, exist_ok=True)
    chid = f"{cdir}-ch{ch_no:02d}"
    meta = []
    for k, L in enumerate(lessons, 1):
        lid = f"{chid}-l{k:02d}"
        check_lesson(lid, L["screens"])
        doc = {"schema_version": "1.0", "site": SITE, "level": 1,
               "course": {"id": cdir, "title": course_title},
               "chapter": {"id": chid, "no": ch_no, "title": ch_title},
               "lesson": {"id": lid, "no": k, "title": L["title"], "minutes": L.get("minutes", 15)},
               "tags": {"domain": L["domain"], "region": "KR", "curriculum": curriculum},
               "screens": L["screens"]}
        json.dump(doc, open(os.path.join(d, f"l{k:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        meta.append({"no": k, "id": lid, "title": L["title"], "file": f"l{k:02d}.json",
                     "questions": sum(s["type"] == "question" for s in L["screens"]), "screens": len(L["screens"])})
    rq = []
    for q in review:
        q = dict(q); q["stage"] = "review"
        errs = check_q(q, True)
        if errs: raise SystemExit(f"{chid} 복습: " + ", ".join(errs))
        rq.append(q)
    if len(rq) != 10: raise SystemExit(f"{chid} 복습 문항 {len(rq)}개")
    missing = {m["id"] for m in meta} - {q["source_lesson"] for q in rq}
    if missing: raise SystemExit(f"{chid} 복습에 빠진 레슨: {missing}")
    rdoc = {"schema_version": "1.0", "site": SITE, "level": 1, "course": {"id": cdir, "title": course_title},
            "chapter": {"id": chid, "no": ch_no, "title": ch_title},
            "review": {"id": f"{chid}-review", "title": f"{ch_title} 복습", "minutes": 10}, "questions": rq}
    json.dump(rdoc, open(os.path.join(d, "review.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    chap = {"schema_version": "1.0", "course": cdir, "chapter": {"id": chid, "no": ch_no, "title": ch_title},
            "lessons": meta, "review": {"id": f"{chid}-review", "file": "review.json", "questions": 10}}
    json.dump(chap, open(os.path.join(d, "chapter.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    tq = sum(m["questions"] for m in meta)
    print(f"{chid} {ch_title}: 레슨 {len(meta)}개, 문항 {tq} + 복습 10")
