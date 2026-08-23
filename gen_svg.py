#!/usr/bin/env python3
"""
Generates dark_mode.svg and light_mode.svg for the GitHub profile README
from profile_config.json — so you never have to hand-edit SVG files.

Usage:  python3 gen_svg.py

Layout inspired by Andrew6rant/Andrew6rant (github.com/Andrew6rant/Andrew6rant).
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 60          # visible character width of the right-hand info column
LINE_H = 20         # px per text row
FONT_SIZE = 16
X_ASCII = 15
X_INFO = 390
WIDTH = 985
Y0 = 30

PALETTES = {
    "dark_mode.svg": {
        "bg": "#161b22", "fg": "#c9d1d9", "key": "#ffa657", "value": "#a5d6ff",
        "add": "#3fb950", "del": "#f85149", "cc": "#616e7f",
    },
    "light_mode.svg": {
        "bg": "#f6f8fa", "fg": "#24292f", "key": "#953800", "value": "#0a3069",
        "add": "#1a7f37", "del": "#cf222e", "cc": "#c2cfde",
    },
}


def rule(prefix: str) -> str:
    """'name' -> 'name -——————…-—-' padded to TOTAL chars."""
    pad = TOTAL - len(prefix) - 1
    return prefix + " -" + "—" * (pad - 4) + "-—-"


def key_tspans(key: str) -> str:
    """Render 'Languages.Programming' as key-coloured tspans joined by plain dots."""
    return ".".join(f'<tspan class="key">{escape(part)}</tspan>' for part in key.split("."))


def dots_for(key: str, value: str) -> int:
    n = TOTAL - 2 - len(key) - 1 - 2 - len(value)
    if n < 1:
        raise ValueError(f"Line too long ({-n} chars over): {key}: {value}")
    return n


def kv_line(key: str, value: str, value_id: str = None) -> str:
    n = dots_for(key, value)
    id_dots = f' id="{value_id}_dots"' if value_id else ""
    id_val = f' id="{value_id}"' if value_id else ""
    return (f'<tspan class="cc">. </tspan>{key_tspans(key)}:'
            f'<tspan class="cc"{id_dots}> {"." * n} </tspan>'
            f'<tspan class="value"{id_val}>{escape(value)}</tspan>')


def stats_line_1(repos: str, contrib: str, stars: str) -> str:
    fixed = 2 + 5 + 1 + len(repos) + 15 + len(contrib) + 4 + 5 + 1 + len(stars)
    left = TOTAL - fixed - 2 - 2  # two dot-blocks, each padded by 2 spaces
    d1 = max(1, min(4, left // 3))
    d2 = max(1, left - d1)
    return (f'<tspan class="cc">. </tspan><tspan class="key">Repos</tspan>:'
            f'<tspan class="cc" id="repo_data_dots"> {"." * d1} </tspan>'
            f'<tspan class="value" id="repo_data">{escape(repos)}</tspan>'
            f' {{<tspan class="key">Contributed</tspan>: '
            f'<tspan class="value" id="contrib_data">{escape(contrib)}</tspan>}} | '
            f'<tspan class="key">Stars</tspan>:'
            f'<tspan class="cc" id="star_data_dots"> {"." * d2} </tspan>'
            f'<tspan class="value" id="star_data">{escape(stars)}</tspan>')


def stats_line_2(commits: str, followers: str) -> str:
    fixed = 2 + 7 + 1 + len(commits) + 3 + 9 + 1 + len(followers)
    left = TOTAL - fixed - 2 - 2
    d2 = max(1, min(7, left // 3))
    d1 = max(1, left - d2)
    return (f'<tspan class="cc">. </tspan><tspan class="key">Commits</tspan>:'
            f'<tspan class="cc" id="commit_data_dots"> {"." * d1} </tspan>'
            f'<tspan class="value" id="commit_data">{escape(commits)}</tspan>'
            f' | <tspan class="key">Followers</tspan>:'
            f'<tspan class="cc" id="follower_data_dots"> {"." * d2} </tspan>'
            f'<tspan class="value" id="follower_data">{escape(followers)}</tspan>')


def stats_line_3(loc: str, loc_add: str, loc_del: str) -> str:
    label = "Lines of Code on GitHub"
    fixed = 2 + len(label) + 1 + len(loc) + 3 + len(loc_add) + 4 + len(loc_del) + 4
    left = TOTAL - fixed - 2
    n = max(1, left)
    return (f'<tspan class="cc">. </tspan><tspan class="key">{label}</tspan>:'
            f'<tspan class="cc" id="loc_data_dots"> {"." * n} </tspan>'
            f'<tspan class="value" id="loc_data">{escape(loc)}</tspan>'
            f' ( <tspan class="addColor" id="loc_add">{escape(loc_add)}</tspan><tspan class="addColor">++</tspan>,'
            f' <tspan class="delColor" id="loc_del">{escape(loc_del)}</tspan><tspan class="delColor">-sub-</tspan> )').replace("-sub-", "--")


def build_info_rows(cfg: dict) -> list:
    s = cfg["stats"]
    rows = [("plain", f'<tspan class="value">{escape(rule(cfg["title"]))}</tspan>')]
    for item in cfg["system"]:
        if item.get("blank"):
            rows.append(("cc", ". "))
        else:
            rows.append(("plain", kv_line(item["key"], item["value"], item.get("id"))))
    rows.append(("plain", f'<tspan class="value">{escape(rule("- Contact"))}</tspan>'))
    for item in cfg["contact"]:
        rows.append(("plain", kv_line(item["key"], item["value"])))
    rows.append(("plain", f'<tspan class="value">{escape(rule("- GitHub Stats"))}</tspan>'))
    rows.append(("plain", stats_line_1(s["repos"], s["contributed"], s["stars"])))
    rows.append(("plain", stats_line_2(s["commits"], s["followers"])))
    rows.append(("plain", stats_line_3(s["loc"], s["loc_add"], s["loc_del"])))
    return rows


def render(cfg: dict, filename: str, palette: dict) -> str:
    ascii_lines = cfg["ascii"]
    info_rows = build_info_rows(cfg)
    n_rows = max(len(ascii_lines), len(info_rows))
    height = Y0 + (n_rows - 1) * LINE_H + LINE_H

    out = []
    out.append("<?xml version='1.0' encoding='UTF-8'?>")
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" '
               f'width="{WIDTH}px" height="{height}px" font-size="{FONT_SIZE}px">')
    out.append("<style>")
    out.append("@font-face {")
    out.append("src: local('Consolas'), local('Consolas Bold');")
    out.append("font-family: 'ConsolasFallback';")
    out.append("font-display: swap;")
    out.append("-webkit-size-adjust: 109%;")
    out.append("size-adjust: 109%;")
    out.append("}")
    out.append(f'.key {{fill: {palette["key"]};}}')
    out.append(f'.value {{fill: {palette["value"]};}}')
    out.append(f'.addColor {{fill: {palette["add"]};}}')
    out.append(f'.delColor {{fill: {palette["del"]};}}')
    out.append(f'.cc {{fill: {palette["cc"]};}}')
    out.append("text, tspan {white-space: pre;}")
    out.append("</style>")
    out.append(f'<rect width="{WIDTH}px" height="{height}px" fill="{palette["bg"]}" rx="15"/>')

    out.append(f'<text x="{X_ASCII}" y="{Y0}" fill="{palette["fg"]}" class="ascii">')
    for i, line in enumerate(ascii_lines):
        y = Y0 + i * LINE_H
        out.append(f'<tspan x="{X_ASCII}" y="{y}">{escape(line)}</tspan>')
    out.append("</text>")

    out.append(f'<text x="{X_INFO}" y="{Y0}" fill="{palette["fg"]}">')
    for i, (kind, content) in enumerate(info_rows):
        y = Y0 + i * LINE_H
        cls = ' class="cc"' if kind == "cc" else ""
        out.append(f'<tspan x="{X_INFO}" y="{y}"{cls}>{content}</tspan>')
    out.append("</text>")
    out.append("</svg>")
    return "\n".join(out)


def main():
    with open(os.path.join(HERE, "profile_config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    for filename, palette in PALETTES.items():
        path = os.path.join(HERE, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(cfg, filename, palette))
        print(f"wrote {filename}")


if __name__ == "__main__":
    main()
