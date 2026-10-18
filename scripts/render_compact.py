"""Generate matching light/dark banners for the compact profile."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parents[1] / "assets"
data_path = OUT / "profile-data.json"
data = json.loads(data_path.read_text()) if data_path.exists() else {}
project = data.get("current_project", "something new")
for theme, bg, ink, muted, border, accent in [
    ("dark", "#101321", "#f0efff", "#a9adc6", "#30334c", "#c4afff"),
    ("light", "#f8f7ff", "#25243d", "#595773", "#dedbed", "#7152bd"),
]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="172" viewBox="0 0 840 172" role="img" aria-labelledby="title desc">
<title id="title">Torine — Code with logic. Create with color.</title>
<desc id="desc">Java / JVM, Minecraft, AI agents. Currently building {escape(project)}.</desc>
<defs>
  <linearGradient id="accent"><stop stop-color="#59d6de"/><stop offset=".5" stop-color="#ad8aef"/><stop offset="1" stop-color="#f095be"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#a78bea" stop-opacity=".16"/><stop offset="1" stop-color="#a78bea" stop-opacity="0"/></radialGradient>
  <clipPath id="clip"><rect x=".5" y=".5" width="839" height="171" rx="16"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect x=".5" y=".5" width="839" height="171" rx="16" fill="{bg}" stroke="{border}"/>
  <ellipse cx="420" cy="60" rx="380" ry="180" fill="url(#glow)"/>
  <path d="M180 1H660" stroke="url(#accent)" stroke-width="2"/>
  <g fill="none" stroke="url(#accent)" opacity=".45">
    <g transform="translate(116 87)">
      <circle r="42" opacity=".35"/>
      <ellipse rx="63" ry="22" transform="rotate(-38)"/>
      <ellipse rx="63" ry="22" transform="rotate(38)" opacity=".5"/>
      <circle cx="48" cy="-31" r="3" fill="{accent}" stroke="none"/>
    </g>
    <g transform="translate(724 87)">
      <circle r="42" opacity=".35"/>
      <ellipse rx="63" ry="22" transform="rotate(38)"/>
      <ellipse rx="63" ry="22" transform="rotate(-38)" opacity=".5"/>
      <circle cx="-48" cy="-31" r="3" fill="{accent}" stroke="none"/>
    </g>
  </g>
  <g text-anchor="middle" font-family="Segoe UI,Arial,sans-serif">
    <text x="420" y="34" fill="{accent}" font-size="10" letter-spacing="3">DEVELOPER &amp; CREATOR</text>
    <text x="420" y="86" fill="{ink}" font-size="48" font-weight="700">Torine<tspan fill="{accent}">.</tspan></text>
    <text x="420" y="114" fill="{muted}" font-size="15">Code with logic. Create with color.</text>
    <text x="420" y="147" fill="{accent}" font-size="11">CURRENTLY BUILDING / {escape(project[:30])}</text>
  </g>
</g>
</svg>
'''
    (OUT / f"compact-header-{theme}.svg").write_text(svg)
