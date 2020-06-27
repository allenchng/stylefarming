
# Save some images

def scrape(posts):

    # Takes as input a list of styleforum post id's

    for post in posts:
        base_url = "https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/post-"
        image_url = base_url + str(post)

        # test_url = "https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/post-9945141"

        r = requests.get(image_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        html_tag = "#post-" + str(post) + "+ .message-inner .bbImage"

        img = soup.select(html_tag)
        img_url = [image['src'] for image in img]

        # postnum = 9945141

        for index, i in enumerate(img_url):
            if i.startswith('/'):
                url = 'https://www.styleforum.net' + str(i)

                filename = str(post) + "_" + str(index) + ".jpg"
                f = open(filename, 'wb')
                f.write(requests.get(url).content)
                f.close()
            else:
                filename = str(post) + "_" + str(index) + ".jpg"
                f = open(filename, 'wb')
                f.write(requests.get(i).content)
                f.close()

        sleep(randint(1, 3))
