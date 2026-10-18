"""Generate the compact profile banner (no external assets or dependencies)."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parents[1] / "assets"
data_path = OUT / "profile-data.json"
data = json.loads(data_path.read_text()) if data_path.exists() else {}
project = data.get("current_project")
eyebrow = "BUILDING / " + project[:30] if project else "DEVELOPER / CREATOR"

for theme, bg, ink, muted, border, accent in [
    ("dark", "#101321", "#f0efff", "#a9adc6", "#30334c", "#c4afff"),
    ("light", "#f8f7ff", "#25243d", "#595773", "#dedbed", "#7152bd"),
]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="164" viewBox="0 0 840 164" role="img" aria-labelledby="title desc">
  <title id="title">Hi, I'm Torine.</title>
  <desc id="desc">Java / JVM · Minecraft · AI agents. Code with logic. Create with color.</desc>
  <defs>
    <linearGradient id="accent"><stop stop-color="#59d6de"/><stop offset=".5" stop-color="#ad8aef"/><stop offset="1" stop-color="#f095be"/></linearGradient>
    <radialGradient id="glow"><stop stop-color="#a78bea" stop-opacity=".18"/><stop offset="1" stop-color="#a78bea" stop-opacity="0"/></radialGradient>
    <clipPath id="clip"><rect x=".5" y=".5" width="839" height="163" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect x=".5" y=".5" width="839" height="163" rx="16" fill="{bg}" stroke="{border}"/>
    <ellipse cx="702" cy="82" rx="230" ry="150" fill="url(#glow)"/>
    <path d="M32 1H808" stroke="url(#accent)" stroke-width="2"/>
    <g font-family="Segoe UI,Arial,sans-serif">
      <text x="32" y="35" fill="{accent}" font-size="10" letter-spacing="2">{escape(eyebrow)}</text>
      <text x="30" y="82" fill="{ink}" font-size="38" font-weight="700">Hi, I'm Torine<tspan fill="{accent}">.</tspan></text>
      <text x="32" y="111" fill="{muted}" font-size="14">Java / JVM · Minecraft · AI agents</text>
      <text x="32" y="140" fill="{muted}" font-size="12">Code with logic. Create with color.</text>
    </g>
    <g transform="translate(712 82)" fill="none" stroke="url(#accent)">
      <circle r="49" opacity=".25"/>
      <ellipse rx="86" ry="30" transform="rotate(-32)" opacity=".7"/>
      <ellipse rx="86" ry="30" transform="rotate(32)" opacity=".35"/>
      <path d="m-19-13-14 13 14 13m38-26 14 13-14 13m-14-31-10 36" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="65" cy="-38" r="4" fill="{accent}" stroke="none"/>
      <path d="M-97-42v8m-4-4h8M88 40v8m-4-4h8" opacity=".6"/>
    </g>
  </g>
</svg>
'''
    (OUT / f"compact-header-{theme}.svg").write_text(svg)
