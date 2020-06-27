import requests
import pandas as pd
import time

from bs4 import BeautifulSoup
from time import sleep
from random import randint

start = 2785
end = 2787

start_time = time.time()
num_requests = 0

page_url = [str(i) for i in range(start, end)]

# Set up the page features to be scraped

usernames = []
userid = []
day = []
hms_time = []
postnumber = []
likes_postnum = []
likes_count = []
posts = []

for page in page_url:
    url = "https://www.styleforum.net/threads/%D9%AD%D9%AD%D9%AD-no-man-walks-alone-official-affiliate-thread-%D9%AD%D9%AD%D9%AD-a-k-a-i-shouldnt-have-slept-on-it.358758/page-" + str(page)
    response = requests.get(url)
    print("successful request")

    sleep(randint(2, 4))

    num_requests += 1
    # elapsed_time = time.time() - start_time
    # print('Request:{}; Frequency: {} requests/s'.format(num_requests, num_requests / elapsed_time))
    # clear_output(wait=True)

    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(num_requests, response.status_code))

    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape usernames

    users = soup.select('.message-name .username')

    for name in users:
        usernames.append(name.text)

    # Scrape userids

    for username in users:
        userid.append(username["data-user-id"])

    # Scrape date and time for each post

    dt = soup.select('.message-attribution-main .u-dt')

    for title in dt:
        day.append(title.text)

    for time in dt:
        hms_time.append(time["data-time-string"])

    # Scrape unique post id

    links = []
    for elm in soup.find_all('ul', attrs={'class': 'message-attribution-opposite message-attribution-opposite--list'}):
        for a_elm in elm.find_all("a"):
            links.append(a_elm.attrs["href"])

    links_post_num = [s.split('/')[3].strip() for s in links]
    post_num_dupe = [s.split('-')[1].strip() for s in links_post_num]
    post_num = (post_num_dupe[::2])

    for post in post_num:
        postnumber.append(post)

    # Scrape thumbs on each post

    likes_list = []
    for i, li in enumerate(soup.select('.reactionsBar-link')):
        likes_list.append(li.text)

    likes = soup.select('.reactionsBar-link')
    likes_postid = [like['href'] for like in likes]

    for s in likes_postid:
        likes_postnum.append(s.split('/')[2].strip())
    # likes_postnum = [s.split('/')[2].strip() for s in likes_postid]

    num = [s if "others" in s else None for s in likes_list]
    str_num = [s.split()[-2] if s is not None else None for s in num]

    for i in str_num:
        if i is not None:
            likes_count.append(int(i) + 3)
        else:
            likes_count.append(None)
    # like_count = [int(i) + 3 if i is not None else None for i in str_num]

    # Scrape text from each post

    p_text = soup.select('.js-selectToQuote .bbWrapper')

    for post in p_text:
        posts.append(post.text)
    # for post in p_text:
    #     posts.append(post.text)


# Store in dataframe
attribute_df = pd.DataFrame(
    {'username': usernames,
     'date': day,
     'hms': hms_time,
     'post_num': postnumber,
     'post_text': posts
    })

likes_df = pd.DataFrame(
    {'num_likes': likes_count,
     'post_num': likes_postnum
    })

attribute_df.post_num = attribute_df.post_num.astype(int)
likes_df.post_num = likes_df.post_num.astype(int)

full_df = attribute_df.merge(likes_df, on="post_num", how="left")


# if __name__ == '__main__':
#     function_to_write()


# Get top n posts

def top_n_posts(df, n):

    top_onehundred = full_df.sort_values(by='num_likes', ascending=False).head(100)
    posts = full_df["post_num"].tolist()

    top_onehundred = full_df.sort_values(by='num_likes', ascending=False).head(100)
    posts = top_onehundred["post_num"].tolist()

    return posts



# Save some images

# for post in posts:
#     base_url = "https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/post-"
#     image_url = base_url + str(post)
#
#     # test_url = "https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/post-9945141"
#
#     r = requests.get(image_url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#
#     html_tag = "#post-" + str(post) + "+ .message-inner .bbImage"
#
#     img = soup.select(html_tag)
#     img_url = [image['src'] for image in img]
#
#     # postnum = 9945141
#
#     for index, i in enumerate(img_url):
#         if i.startswith('/'):
#             url = 'https://www.styleforum.net' + str(i)
#
#             filename = str(post) + "_" + str(index) + ".jpg"
#             f = open(filename, 'wb')
#             f.write(requests.get(url).content)
#             f.close()
#         else:
#             filename = str(post) + "_" + str(index) + ".jpg"
#             f = open(filename, 'wb')
#             f.write(requests.get(i).content)
#             f.close()
#
#     sleep(randint(1, 3))
