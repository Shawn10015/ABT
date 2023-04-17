import unittest
import vk_api
import datetime
import time
from final_vk import get_posts

class TestGetPosts(unittest.TestCase):

    def setUp(self):
        self.vk_session = vk_api.VkApi(token='your_token')
        self.api = self.vk_session.get_api()

    def test_get_posts(self):
        time_intervals = []
        date = datetime.datetime.now() - datetime.timedelta(days=7)
        for i in range(7):
            start_time = int(time.mktime(date.timetuple()))
            end_time = start_time + 86400  # 86400 sec = 1 day
            time_intervals.append((start_time, end_time))
            date += datetime.timedelta(days=1)

        posts = get_posts(self.api, time_intervals)
        self.assertIsInstance(posts, list)
        for post in posts:
            self.assertIsInstance(post, dict)
            self.assertSetEqual(set(post.keys()), {'id', 'date', 'text', 'likes', 'comments', 'reposts', 'views'})

if __name__ == '__main__':
    unittest.main()