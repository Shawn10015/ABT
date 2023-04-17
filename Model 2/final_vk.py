# -*- coding: utf-8 -*-
import vk_api
import datetime
import time
import json
import pandas as pd


def get_posts(api, time_intervals):
    count = 200
    posts = []

    for i, interval in enumerate(time_intervals):
        start_time, end_time = interval
        offset = 0
        day_posts = []

        while True:
            response = api.newsfeed.search(q='msu', count=count, start_time=start_time, end_time=end_time, offset=offset)

            if isinstance(response, dict) and 'error' in response:
                # If the response is a dictionary and contains an error key, print the error message and exit the program
                print(f"Error occurred: {response['error']['error_msg']}")
                exit()

            day_posts.extend(response['items'])

            offset += count
            if len(response['items']) < count:
                break



        posts += [{
            'id': post['id'],
            'date': datetime.datetime.fromtimestamp(post['date']),
            'text': post['text'],
            'likes': post['likes']['count'] if 'likes' in post else 0,
            'comments': post['comments']['count'] if 'comments' in post else 0,
            'reposts': post['reposts']['count'] if 'reposts' in post else 0,
            'views': post['views']['count'] if 'views' in post else 0,
        } for post in day_posts]

    return posts






if __name__ == '__main__':
    vk_session = vk_api.VkApi(token='your_token')
    api = vk_session.get_api()

    # The date after day=, local time
    time_intervals = []
    date = datetime.datetime(year=2023, month=3, day=1)
    
    for i in range(30):
        start_time = int(time.mktime(date.timetuple()))
        end_time = start_time + 86400  # 86400 sec = 1 day
        time_intervals.append((start_time, end_time))
        date += datetime.timedelta(days=1)


        
    posts = get_posts(api, time_intervals)
    df = pd.DataFrame(posts)
    print(df.head())
    df.to_csv('msu.csv', index=False, encoding='utf-8')

