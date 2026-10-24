"""Translate source descriptions and RSS titles without per-project overrides."""
import hashlib
import re

TRANSLATOR_ID = 'qqtransmart-zh-en/translators-6.0.4/v1'
HAN = re.compile(r'[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0003134f]')


def translate_chinese(source):
    # Only public repository descriptions and RSS titles reach this service.
    # English text and valid cached translations make no translation requests.
    import translators
    return translators.translate_text(
        source, translator='qqTranSmart', from_language='zh', to_language='en',
        timeout=25,
    )


def english_text(value, cache, translate=None):
    source = ' '.join((value or '').split())
    if not source or not HAN.search(source):
        return source
    key = hashlib.sha256(source.encode()).hexdigest()
    cached = cache.get(key, {})
    if (cached.get('source') == source and cached.get('provider') == TRANSLATOR_ID
            and cached.get('english') and not HAN.search(cached['english'])):
        return cached['english']
    english = ' '.join((translate or translate_chinese)(source).split())
    if not english or HAN.search(english):
        raise ValueError('Translation did not produce English; keeping the published profile unchanged')
    cache[key] = {'source': source, 'english': english, 'provider': TRANSLATOR_ID}
    return english
