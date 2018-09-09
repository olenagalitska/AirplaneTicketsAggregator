import threading
import time


class UpdaterStarter(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.isWorking = True

    def run(self):
        time.sleep(10)

        from app.updaters.airlines_info_updater import AirlinesInfoUpdater
        from app.updaters.airlines_news_updater import AirlinesNewsUpdater
        from app.updaters.flights_updater import FlightsUpdater

        airlines_news_updater = AirlinesNewsUpdater("Airlines News Updater")
        airlines_news_updater.start()

        airlines_info_updater = AirlinesInfoUpdater("Airlines Info Updater")
        airlines_info_updater.start()

        flights_updater = FlightsUpdater("Flights Updater")
        flights_updater.start()
