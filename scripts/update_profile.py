"""Refresh public profile data. Run with GH_TOKEN or an authenticated gh CLI."""
import json
import re
import runpy
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse
from profile_descriptions import HAN, english_text

ROOT = Path(__file__).resolve().parents[1]
OWNER = "windy664"


def safe_link(value):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in {
        "windy664.github.io", "github.com"
    }:
        raise ValueError(f"Unexpected public URL: {value}")
    return escape(value, quote=True)


def text(value):
    return escape(" ".join(value.split()), quote=True)


def replace_section(readme, name, body):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise ValueError(f"Missing or duplicate markers: {name}")
    return re.sub(re.escape(start) + r".*?" + re.escape(end),
                  lambda _: f"{start}\n{body}\n{end}", readme, flags=re.S)


def latest_posts(feed, now):
    posts = []
    for item in feed.findall('./channel/item'):
        published = parsedate_to_datetime(item.findtext('pubDate'))
        title = item.findtext('title', '').strip()
        url = item.findtext('link', '').strip()
        if not title or not url:
            raise ValueError('RSS item is missing its title or link')
        if published <= now:
            posts.append((published, title, url))
    posts.sort(key=lambda post: post[0], reverse=True)
    if len(posts) < 2:
        raise ValueError('Expected at least two published blog posts')
    return posts[:2]


def profile_data(repos, posts, translations):
    data = {'current_project': repos[0]['name'], 'projects': [], 'posts': []}
    for repo in repos:
        description = repo['description'] or ''
        data['projects'].append({
            'name': repo['name'], 'url': repo['html_url'],
            'language': repo['language'] or 'Code',
            'description': description,
            'summary': english_text(description, translations),
        })
    for date, title, url in posts:
        data['posts'].append({
            'source_title': title,
            'title': english_text(title, translations),
            'url': url, 'date_label': date.strftime('%b %d'),
            'published_at': date.isoformat(),
            'source_language': 'zh' if HAN.search(title) else 'en',
        })
    return data


def main():
    request = urllib.request.Request(
        "https://windy664.github.io/rss.xml", headers={"User-Agent": "Torine-Profile"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        feed = ET.fromstring(response.read())
    posts = latest_posts(feed, datetime.now(timezone.utc))

    result = subprocess.run(
        ["gh", "api", f"users/{OWNER}/repos?sort=pushed&per_page=100"],
        check=True, capture_output=True, text=True,
    )
    repos = [repo for repo in json.loads(result.stdout)
             if not repo["fork"] and not repo["archived"] and not repo["private"]
             and repo["name"] not in {OWNER, f"{OWNER}.github.io", "github-workflow-practice"}]
    repos.sort(key=lambda repo: repo["pushed_at"], reverse=True)
    repos = repos[:2]
    if len(repos) < 2:
        raise ValueError("Expected at least two public projects")

    cache_path = ROOT / 'assets/profile-translations.json'
    translations = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    data = profile_data(repos, posts, translations)
    journal = []
    for kind, label in [('projects', 'On my desk'), ('posts', 'Recent posts')]:
        journal.extend([f'<h4>{label}</h4>', '<p>'])
        for index, item in enumerate(data[kind]):
            asset = f'https://raw.githubusercontent.com/{OWNER}/{OWNER}/master/assets/profile-{kind}-{index}'
            alt = (item['name'] + (' — ' + item['summary'] if item['summary'] else '')
                   if kind == 'projects' else item['title'] +
                   (' (article in Chinese)' if item['source_language'] == 'zh' else ''))
            journal.append(
                f'<a href="{safe_link(item["url"])}"><picture>'
                f'<source media="(prefers-color-scheme: dark)" srcset="{asset}-dark.svg" />'
                f'<img src="{asset}-light.svg" width="410" alt="{text(alt)}" />'
                '</picture></a>'
            )
        journal.append('</p>')
    readme = (ROOT / "README.md").read_text()
    readme = replace_section(readme, "JOURNAL", '\n'.join(journal))
    (ROOT / "assets/profile-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    runpy.run_path(str(ROOT / "scripts/render_compact.py"))
    (ROOT / "README.md").write_text(readme)
    cache_path.write_text(json.dumps(translations, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
    print("Updated two blog posts, two public projects, and both banner themes.")


if __name__ == "__main__":
    main()
