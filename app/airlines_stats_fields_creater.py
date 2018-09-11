import threading
import time

from app.dbmanager.airlines_manager import AirlinesManager


class AirlinesStatsFieldsCreater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True
        self.airlines_manager = AirlinesManager()

    def run(self):
        time.sleep(10)
        # print('Airlines Stats Fields Creater started')
        while self.isWorking:
            self.airlines_manager.create_stats_fields()
            time.sleep(60 * 60 * 24 * 365)

    def stop(self):
        self.isWorking = False
