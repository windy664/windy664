# Profile refresh

`update_profile.py` selects the two most recently pushed public repositories,
excluding forks, archived repositories, this profile, the blog, and the workflow
practice repository. The workflow runs daily at 01:23 UTC and can also be started
manually in GitHub Actions.

Project descriptions come only from the GitHub repository's **About → Description**
field. There are no per-project description overrides. English text, including
emoji and typographic punctuation, is preserved. Missing descriptions stay empty.
`assets/profile-data.json` retains the original `description` and display `summary`;
the SVG shows at most two lines, while the image's alternative text keeps the full
display summary.

Blog dates, links and original titles come directly from the latest two published
RSS entries. `source_title` records the original; `title` is its English translation.
There are no title overrides or generic "Field notes" substitutes.

Chinese descriptions and titles use Google Translate through
[deep-translator](https://github.com/nidhaloff/deep-translator), with Tencent
TranSmart through [Translators](https://github.com/UlionTse/translators) as a fallback.
Only these public source texts are sent to the services; no API key is needed.
Google has a 35-second overall deadline and Tencent requests a 25-second timeout.
Certificate validation stays enabled. If both services fail, the refresh fails
instead of producing placeholder content. Translations, including the engine
actually used, are saved in
`assets/profile-translations.json`, keyed by the source text hash and checked
against the provider version. Changed or removed source text never reuses old text.
Machine translations may be imperfect; an English repository description bypasses
translation completely.

If fetching or translating fails, the workflow fails before committing the update,
so the published profile remains at its last successful version. It retries at the
next scheduled or manual run.

Run locally with Python 3.12 and an authenticated `gh` CLI:

```sh
python3 -m pip install -r scripts/requirements-profile.txt
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/update_profile.py
```
