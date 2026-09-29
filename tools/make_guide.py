"""레벨2·3 가이드 페이지(guide.html) 생성. 플레이어를 고친 뒤 다시 실행한다.
사용: python3 tools/make_guide.py [사이트 경로]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import render

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
player = open(os.path.join(SITE, "player.html"), encoding="utf-8").read()
tpl = open(os.path.join(HERE, "guide_tpl.html"), encoding="utf-8").read()
page = render(tpl, player)
open(os.path.join(SITE, "guide.html"), "w", encoding="utf-8").write(page)
print(f"가이드 페이지: {os.path.join(SITE, 'guide.html')} ({len(page):,}바이트)")
