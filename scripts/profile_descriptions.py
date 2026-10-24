"""Translate source descriptions and RSS titles without per-project overrides."""
import hashlib
import re
import subprocess
import sys

TRANSLATOR_ID = 'google-qqtransmart-zh-en/v2'
HAN = re.compile(r'[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0003134f]')


def translate_chinese(source):
    # Only public repository descriptions and RSS titles reach this service.
    # English text and valid cached translations make no translation requests.
    try:
        # Isolate the web client so its HTTP requests have an overall deadline.
        result = subprocess.run(
            [sys.executable, '-c',
             'from deep_translator import GoogleTranslator; import sys; '
             'print(GoogleTranslator(source="zh-CN", target="en").translate(sys.stdin.read()))'],
            input=source, capture_output=True, text=True, check=True, timeout=35,
        ).stdout.strip()
        if result and not HAN.search(result):
            return result, 'google'
    except (subprocess.SubprocessError, OSError) as error:
        print(f'Google translation unavailable ({type(error).__name__}); trying Tencent.', file=sys.stderr)
    import translators
    result = translators.translate_text(
        source, translator='qqTranSmart', from_language='zh', to_language='en', timeout=25,
    )
    return result, 'qqtransmart'


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
