import unittest
from unittest.mock import Mock

from profile_descriptions import english_text


class ProjectDescriptionsTest(unittest.TestCase):
    def test_english_with_emoji_and_unicode_punctuation_is_preserved(self):
        description = '🤖 Rust + Codex — automation, photos & messaging.'
        translate = Mock(side_effect=AssertionError('English must not be translated'))
        self.assertEqual(english_text(description, {}, translate), description)
        translate.assert_not_called()

    def test_changed_english_description_is_reflected_immediately(self):
        cache = {}
        self.assertEqual(english_text('Old purpose.', cache), 'Old purpose.')
        self.assertEqual(english_text('New purpose.', cache), 'New purpose.')

    def test_missing_or_removed_description_is_empty(self):
        for value in (None, '', '  \n '):
            self.assertEqual(english_text(value, {}), '')

    def test_translation_is_reused_only_for_the_same_source(self):
        translate = Mock(side_effect=['A Minecraft plugin.', 'A server tool.'])
        cache = {}
        self.assertEqual(english_text('一个 Minecraft 插件。', cache, translate), 'A Minecraft plugin.')
        self.assertEqual(english_text('一个 Minecraft 插件。', cache, translate), 'A Minecraft plugin.')
        self.assertEqual(translate.call_count, 1)
        self.assertEqual(english_text('一个服务器工具。', cache, translate), 'A server tool.')
        self.assertEqual(translate.call_count, 2)
        self.assertEqual(english_text(None, cache, translate), '')

    def test_failed_translation_does_not_reuse_an_old_description(self):
        cache = {}
        english_text('旧简介。', cache, lambda _: 'Old description.')
        translate = Mock(side_effect=RuntimeError('Model unavailable'))
        with self.assertRaises(RuntimeError):
            english_text('新简介。', cache, translate)
        self.assertEqual(len(cache), 1)

    def test_changed_provider_invalidates_a_cached_translation(self):
        cache = {}
        english_text('一个插件。', cache, lambda _: 'An old translation.')
        next(iter(cache.values()))['provider'] = 'retired-provider'
        self.assertEqual(english_text('一个插件。', cache, lambda _: 'A new translation.'),
                         'A new translation.')

    def test_empty_or_untranslated_results_are_not_cached(self):
        for result in ('', '这是中文。'):
            cache = {}
            with self.assertRaises(ValueError):
                english_text('需要翻译。', cache, lambda _: result)
            self.assertEqual(cache, {})


if __name__ == '__main__':
    unittest.main()
