"""Translate source descriptions and RSS titles without per-project overrides."""
import hashlib
import json
import re
import urllib.request
from html import unescape
from urllib.parse import urlencode

TRANSLATOR_ID = 'mymemory-zh-en/v1'
HAN = re.compile(r'[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0003134f]')


def utf8_segments(source, limit=500):
    """Respect the service's byte limit without dropping source characters."""
    while source:
        size = 0
        end = 0
        for char in source:
            size += len(char.encode('utf-8'))
            if size > limit:
                break
            end += 1
        if end < len(source):
            boundaries = list(re.finditer(r'[\s，。！？,;.!?]', source[:end]))
            if boundaries and boundaries[-1].end() > end // 2:
                end = boundaries[-1].end()
        yield source[:end]
        source = source[end:]


def translate_chinese(source):
    # Only public repository descriptions and RSS titles reach this service.
    # English text and valid cached translations make no translation requests.
    translated = []
    for segment in utf8_segments(source):
        query = urlencode({'q': segment, 'langpair': 'zh-CN|en-US', 'mt': '1'})
        request = urllib.request.Request(
            'https://api.mymemory.translated.net/get?' + query,
            headers={'User-Agent': 'Torine-Profile/1.0'},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        if data.get('quotaFinished') or str(data.get('responseStatus')) != '200':
            raise RuntimeError(f'Translation service rejected the request: {data.get("responseStatus")}')
        result = unescape(data.get('responseData', {}).get('translatedText', '')).strip()
        if not result or HAN.search(result):
            raise ValueError('Translation service did not return English text')
        translated.append(result)
    return ' '.join(translated), 'mymemory'


def english_text(value, cache, translate=None):
    source = ' '.join((value or '').split())
    if not source or not HAN.search(source):
        return source
    key = hashlib.sha256(source.encode()).hexdigest()
    cached = cache.get(key, {})
    if (cached.get('source') == source and cached.get('provider') == TRANSLATOR_ID
            and cached.get('english') and not HAN.search(cached['english'])):
        return cached['english']
    translated = (translate or translate_chinese)(source)
    value, engine = translated if isinstance(translated, tuple) else (translated, TRANSLATOR_ID)
    english = ' '.join(value.split())
    if not english or HAN.search(english):
        raise ValueError('Translation did not produce English; keeping the published profile unchanged')
    cache[key] = {'source': source, 'english': english, 'provider': TRANSLATOR_ID, 'engine': engine}
    return english
