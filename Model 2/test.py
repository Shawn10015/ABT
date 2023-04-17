# -*- coding: utf-8 -*-


import vk_api
import datetime
import time
import json 

vk_session = vk_api.VkApi(token='your_token')
api = vk_session.get_api()

#The date after day=, local time
date = datetime.datetime(year=2023, month=3, day=14)  
start_time = int(time.mktime(date.timetuple()))
end_time = start_time + 86400
#86400  


count = 200
offset = 0
posts = []

while True:
    response = api.newsfeed.search(q='msu', count=count, start_time=start_time, end_time=end_time, offset=offset)
    
    if isinstance(response, dict) and 'error' in response:
        # If the response is a dictionary and contains an error key, print the error message and exit the program
        print(f"Error occurred: {response['error']['error_msg']}")
        exit()
    

    posts += response['items']
    

    offset += count
    if len(response['items']) < count:
        break


with open('posts.txt', 'w', encoding='utf-8') as file:
    for post in posts:
        file.write(str(post) + '\n')


posts_json = json.dumps(posts, indent=4, ensure_ascii=False)


with open('spbu_posts.txt', 'w', encoding='utf-8') as f:
    f.write(posts_json)


num_posts = len(posts)
num_likes = sum([post['likes']['count'] for post in posts])
num_reposts = sum([post['reposts']['count'] for post in posts])
num_comments = sum([post['comments']['count'] for post in posts])

num_views = 0
for post in posts:
    if 'views' in post:
        num_views += post['views']['count']


print(f"Number of posts: {num_posts}")
print(f"Number of likes: {num_likes}")
print(f"Number of views: {num_views}")
print(f"Number of shares: {num_reposts}")
print(f"Number of comments: {num_comments}")