"""Build the animated SVG intro. Run: python3 scripts/build_intro.py"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACE = 1.4
# x, y, width, height, delay, speaker, lines
MESSAGES = [
    (28, 84, 205, 46, .35, "nam", ["Hey, I'm Nam."]),
    (28, 142, 574, 68, 1.1, "nam", [
        "I build AI experiments, robotics projects,",
        "and tools that make the results easier to explore."]),
    (390, 224, 342, 44, 2.15, "guest", ["What are you building lately?"]),
    (28, 282, 600, 68, 3.0, "nam", [
        "PatchBench: a workbench for coding agents.",
        "Build bug-fix tasks. Run agents. Inspect the evidence."]),
    (28, 362, 563, 68, 4.0, "nam", [
        "I also explore how robots respond to language",
        "and tell interactive stories with data."]),
    (28, 442, 492, 46, 5.0, "nam", [
        "A few things from my workbench, below. ↘"]),
]

def render(dark):
    c = ({
        "bg": "#0d1117", "border": "#30363d", "text": "#e6edf3",
        "muted": "#919ba8", "bubble": "#212830", "accent": "#a5b4fc",
        "badge": "#272841", "guest": "#3748a0", "line": "#212830",
    } if dark else {
        "bg": "#ffffff", "border": "#d1d9e0", "text": "#202b3a",
        "muted": "#627084", "bubble": "#f0f3f7", "accent": "#4f46a5",
        "badge": "#efedff", "guest": "#4858bd", "line": "#eaeef2",
    })
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="544" viewBox="0 0 760 544" role="img" aria-labelledby="title desc">
<title id="title">Hi, I'm Nam — AI, robotics, and things you can explore</title>
<desc id="desc">A short animated conversation about Nam's work: PatchBench for coding-agent evaluation, robot learning with SmolVLA, and interactive data stories. Links and demos follow below.</desc>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: {c['text']}; font-size: 19px; }}
.muted {{ fill: {c['muted']}; font-size: 12px; letter-spacing: 1.6px; }}
.message {{ animation: arrive .45s cubic-bezier(.2,.7,.2,1) backwards; }}
.typing {{ opacity: 0; animation: typing 1s linear; }}
.dot {{ fill: {c['muted']}; animation: pulse .7s ease-in-out infinite alternate; }}
@keyframes arrive {{ from {{ opacity: 0; transform: translateY(7px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes typing {{ 0%, 85% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
@keyframes pulse {{ from {{ opacity: .35; }} to {{ opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ .message {{ animation: none; }} .typing {{ display: none; }} .dot {{ animation: none; }} }}
</style>
<rect x=".5" y=".5" width="759" height="543" rx="18" fill="{c['bg']}" stroke="{c['border']}"/>
<rect x="28" y="20" width="34" height="34" rx="11" fill="{c['badge']}"/>
<text x="45" y="43" text-anchor="middle" style="fill:{c['accent']};font-size:19px;font-weight:700">N.</text>
<text x="75" y="34" style="font-size:15px;font-weight:650">Nam / Namprire</text>
<text x="75" y="51" style="fill:{c['muted']};font-size:12px">A quick introduction</text>
<text x="731" y="41" text-anchor="end" class="muted">THE OPEN NOTEBOOK</text>
<path d="M28 68H732" stroke="{c['line']}"/>
''']
    for i, (x, y, width, height, delay, speaker, lines) in enumerate(MESSAGES):
        delay = round(delay * PACE, 2)
        fill = c["guest"] if speaker == "guest" else c["bubble"]
        if i in (1, 3):
            parts.append(f'<g transform="translate({x} {y})"><g class="typing" style="animation-delay:{delay - 1}s"><rect width="70" height="44" rx="18" fill="{fill}"/>')
            for j in range(3):
                parts.append(f'<circle class="dot" cx="{23 + j * 12}" cy="22" r="3.5" style="animation-delay:{j * .16}s"/>')
            parts.append('</g></g>')
        parts.append(f'<g transform="translate({x} {y})"><g class="message" style="animation-delay:{delay}s"><rect width="{width}" height="{height}" rx="18" fill="{fill}"/>')
        for j, line in enumerate(lines):
            style = "fill:#ffffff" if speaker == "guest" else ""
            if i == 3 and j == 0:
                style = f"fill:{c['accent']};font-weight:650"
            parts.append(f'<text x="18" y="{29 + j * 24}" style="{style}">{escape(line)}</text>')
        parts.append('</g></g>')
    parts.append(f'''<text x="29" y="521" class="muted" style="font-size:10px;letter-spacing:1.35px">AI EVALUATION / ROBOT LEARNING / DATA STORIES</text>
<path d="M697 511H730M723 504L730 511L723 518" stroke="{c['accent']}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
''')
    return "\n".join(parts)

if __name__ == "__main__":
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for dark in (False, True):
        (assets / ("intro-dark.svg" if dark else "intro-light.svg")).write_text(render(dark))
