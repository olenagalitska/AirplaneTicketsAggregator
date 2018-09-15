import subprocess
import threading
import time


class AirlinesNewsUpdater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def run(self):
        print('Airlines News Updater started')
        while self.isWorking:
            subprocess.run(['scrapy', 'crawl', 'airlines_news_spider'], cwd='scraping')
            time.sleep(60 * 60 * 3)

    def stop(self):
        self.isWorking = False
