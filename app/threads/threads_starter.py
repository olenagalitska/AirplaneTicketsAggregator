import threading
import time


class ThreadsStarter(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def run(self):
        time.sleep(5)

        from app.threads.airlines_info_updater import AirlinesInfoUpdater
        from app.threads.airlines_news_updater import AirlinesNewsUpdater
        from app.threads.flights_updater import FlightsUpdater
        from app.threads.stats_fields_creater import StatsFieldsCreater

        stats_field_creater = StatsFieldsCreater("Stats Fields Creater")
        # stats_field_creater.start()

        airlines_news_updater = AirlinesNewsUpdater("Airlines News Updater")
        # airlines_news_updater.start()

        airlines_info_updater = AirlinesInfoUpdater("Airlines Info Updater")
        # airlines_info_updater.start()

        flights_updater = FlightsUpdater("Flights Updater")
        # flights_updater.start()


