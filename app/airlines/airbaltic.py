import subprocess

class AirBalticInfoRobber():
    def get_flights(self, results, depart, arrive, date, adults, children, infants):
        subprocess.run(['scrapy', 'crawl', 'airBaltic', '-a', 'depart=' + depart, '-a', 'arrival=' + arrive,
                        '-a', 'adults=' + adults, '-a', 'children=' + children, '-a',
                        'infants=' + infants, '-a', 'date=' + date], cwd='scraping')