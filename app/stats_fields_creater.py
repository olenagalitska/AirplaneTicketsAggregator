import threading
import time

from app.dbmanager.airlines_manager import AirlinesManager
from app.dbmanager.destinations_stats_manager import DestinationsStatsManager


class StatsFieldsCreater(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True
        self.airlines_manager = AirlinesManager()
        self.destinations_stats_manager = DestinationsStatsManager()

    def run(self):
        time.sleep(10)
        # print('Airlines Stats Fields Creater started')
        while self.isWorking:
            self.airlines_manager.create_stats_fields()
            self.destinations_stats_manager.create_stats_fields()
            time.sleep(60 * 60 * 24 * 365)

    def stop(self):
        self.isWorking = False
