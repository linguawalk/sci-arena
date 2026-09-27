"""player.html에서 공용 코드(스타일, 채점·그림 코드)를 뽑아 다른 페이지 템플릿에 끼워 넣는다."""
import re


def extract(player_html):
    css = re.search(r"<style>(.*?)</style>", player_html, re.S).group(1)
    kit = re.search(r"/\* ==KIT-START== \*/(.*?)/\* ==KIT-END== \*/", player_html, re.S).group(1)
    extra = []
    for name in ["const esc", "function answerText", "function solHtml"]:
        i = player_html.index(name)
        j = player_html.index("\n}\n", i) + 3 if name.startswith("function") else player_html.index("\n", i) + 1
        extra.append(player_html[i:j])
    return css, kit + "\n" + "".join(extra)


def render(template, player_html):
    css, js = extract(player_html)
    return template.replace("/*__PLAYER_CSS__*/", css).replace("/*__KIT__*/", js)
