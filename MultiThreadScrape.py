from threading import Thread
from Queue import Queue
import requests

def scraper_worker(q):
    while not q.empty():
        url = q.get()
        r = requests.get(url)
        page = pyquery(r.text)
        data = page("#data").text()
        # do something with data
        q.task_done()

urls = ["https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/page-2489", 
"https://www.styleforum.net/threads/the-what-are-you-wearing-today-waywt-discussion-thread-part-ii.394687/page-2450"]

# Create a queue and fill it
q = Queue()
map(q.put, urls)

# Create 5 scraper workers
for i in range(5):
    t = Thread(target=scraper_worker, args=(q, ))
    t.start()
q.join()