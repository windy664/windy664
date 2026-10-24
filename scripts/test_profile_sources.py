import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from unittest.mock import patch

from update_profile import latest_posts, profile_data


class ProfileSourcesTest(unittest.TestCase):
    def test_latest_rss_entries_are_selected_by_date_and_future_items_excluded(self):
        feed = ET.fromstring('''<rss><channel>
          <item><title>Older</title><link>https://windy664.github.io/old/</link><pubDate>Mon, 19 Oct 2026 04:00:00 GMT</pubDate></item>
          <item><title>Future</title><link>https://windy664.github.io/future/</link><pubDate>Mon, 26 Oct 2026 04:00:00 GMT</pubDate></item>
          <item><title>Newest real title</title><link>https://windy664.github.io/new/</link><pubDate>Sat, 24 Oct 2026 04:00:00 GMT</pubDate></item>
          <item><title>Previous real title</title><link>https://windy664.github.io/previous/</link><pubDate>Tue, 20 Oct 2026 04:00:00 GMT</pubDate></item>
        </channel></rss>''')
        result = latest_posts(feed, datetime(2026, 10, 24, 12, tzinfo=timezone.utc))
        self.assertEqual([post[1] for post in result], ['Newest real title', 'Previous real title'])
        self.assertEqual(result[0][2], 'https://windy664.github.io/new/')

    def test_known_names_and_urls_never_override_updated_source_text(self):
        repos = [{'name': 'Ru41', 'html_url': 'https://github.com/windy664/Ru41',
                  'language': 'Rust', 'description': 'A completely revised purpose — from GitHub.'}]
        posts = [(datetime(2026, 10, 19, tzinfo=timezone.utc), 'A changed title — from RSS',
                  'https://windy664.github.io/2026/10/19/p-818d804909c3/')]
        data = profile_data(repos, posts, {})
        self.assertEqual(data['projects'][0]['summary'], repos[0]['description'])
        self.assertEqual(data['posts'][0]['title'], posts[0][1])
        self.assertEqual(data['posts'][0]['source_title'], posts[0][1])

    def test_chinese_project_and_blog_use_the_same_translation_pipeline(self):
        repos = [{'name': 'NewRepo', 'html_url': 'https://github.com/windy664/NewRepo',
                  'language': 'Java', 'description': '仓库里的新简介'}]
        posts = [(datetime(2026, 10, 24, tzinfo=timezone.utc), 'RSS 里的新标题',
                  'https://windy664.github.io/new/')]
        with patch('update_profile.english_text', side_effect=['Translated description', 'Translated title']) as translate:
            data = profile_data(repos, posts, {})
        self.assertEqual([call.args[0] for call in translate.call_args_list],
                         ['仓库里的新简介', 'RSS 里的新标题'])
        self.assertEqual(data['projects'][0]['description'], '仓库里的新简介')
        self.assertEqual(data['projects'][0]['summary'], 'Translated description')
        self.assertEqual(data['posts'][0]['source_title'], 'RSS 里的新标题')
        self.assertEqual(data['posts'][0]['title'], 'Translated title')
        self.assertEqual(data['posts'][0]['source_language'], 'zh')


if __name__ == '__main__':
    unittest.main()
