import subprocess
import threading
import time


class AirlinesInfoUpdater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def run(self):
        time.sleep(30)
        print('Airlines Info Updater started')
        while self.isWorking:
            subprocess.check_output(['scrapy', 'crawl', 'airlines_info_spider'])

            time.sleep(60 * 60 * 24 * 3)

    def stop(self):
        self.isWorking = False
