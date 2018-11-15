import requests
import json
from app import logger
import datetime


class EasyJetInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date, adults, children, infants, teens):
        logger.info('in method')
        date_str = date
        format_str = '%d-%m-%Y'
        datetime_obj = datetime.datetime.strptime(date_str, format_str)
        date = datetime_obj.date()
        logger.debug(
            'depart: ' + str(depart) + '; arrive: ' + str(arrive) + '; date: ' + str(date_str) + '; adults: ' + str(
                adults) + '; children: ' + str(children) + '; infants: ' + str(infants) + '; teens: ' + str(teens))
        data = {
            'AdultSeats': adults,
            'ChildSeats': children + teens,
            'Infants': infants,
            'DateOut': date,
            'DepartureIata': depart,
            'ArrivalIata': arrive,
            "IncludeAdminFees": "true",
            "IncludeFlexiFares": "false",
            "IncludeLowestFareSeats": "true",
            "IncludePrices": "true",
            'FlexDaysOut': '0',  # change to check whole month
            'IncludeConnectingFlights': 'false',
            "IsTransfer": "false",
            "AdditionalSeats": "0",
            "LanguageCode": "EN",
            "MaxDepartureDate": date,
            "MinDepartureDate": date
        }
        headers = {
            'Cookie': "CMSPOD=fra-sc2-blue; bm_sz=1182C38634CCDC3BD0D8967E6460CABF~QAAQZDQWApt9OtRmAQAA9Y7wF+W8T8PPboKZSZOO2qGpF4fvyyhz+HijkcXrdT0nLrZ7qX5i20BUe/9keurs06umw589533pnv0Vc5kdA6agnG3T7fJAbtiaw+nLZ9in5wZJB21mHdkGsnEopyr7siTiwnIjHuKJOEP+cKS+nmoboM2Yohgc8nNX7AozIbxu; cookies.js=1; _ga=GA1.3.20522317.1542294902; _gid=GA1.3.1173258440.1542294902; _gat=1; _abck=ED23A85B49122FCE76C748C6C6B70CDF02163464CB360000748DED5B9C23DE2F~0~OYs9gWxDRBF44x/9Oz8R0JIxX58OHO3Hr4ZvDLXmfKc=~-1~-1; RBKPOD=dub-rbk-blue; odb*=LUZ; ak_bmsc=DA78E3A676C0F5C7CFA3DC101C5C448802163464CB360000748DED5BA3C9FB3B~pl5lUgykgTk+m3G16z4vWtQSrOwWqBxsha3Qe03k7SdSY5fKI4I/HtwuXQxe2l5569KrufO3BoKH1FVEqTGDX5n31UTBI3NlUjFm+oVlxBu5UQtr0m2jEGh1CVQ7hNJEEQY+AuN1t6bEUY0Z7CAF4z+waLfGL2ncCciMpag4n816LVyVAqBAAdIo1eVNDbQ1QqQPnQXvNlBHG1QfDbWKj7BJYM6aMvGiT12Bh6VI/ynu2iUmWdVOjjuPPB67xfC9SA; 47620=; lang2012=de-de; idb*=%7B%22departure%22%3Anull%2C%22when%22%3Anull%2C%22flag%22%3Anull%2C%22price%22%3Anull%2C%22destination%22%3Anull%2C%22fromDate%22%3Anull%2C%22toDate%22%3Anull%2C%22customDate%22%3Anull%2C%22mapLocation%22%3Anull%2C%22moveMap%22%3Anull%2C%22region%22%3A%22de-de%22%7D; _gcl_au=1.1.2078791191.1542294906; __qca=P0-1157098649-1542294906367; ejCC_3=v=5103873542100056430&i=-8586593119773884272; WPPOD=2; cookies_accepted=1; ADRUM=s=1542294931504&r=https%3A%2F%2Fwww.easyjet.com%2Fde%2F%3F0; ADRUM_BTa=R:27|g:b6fe2228-4a34-4efe-9e36-1bc045f416cd; ADRUM_BT1=R:27|i:3126|e:49; FunnelQuery=%7b%22OriginIata%22%3a%22WAW%22%2c%22DestinationIata%22%3a%22*BR%22%2c%22OutboundDate%22%3a%222018-11-15%22%2c%22ReturnDate%22%3anull%2c%22OutboundFlightNumber%22%3anull%2c%22ReturnFlightNumber%22%3anull%2c%22FunnelJourney%22%3a%22defaultwithoffers%22%2c%22UsingFixedJourney%22%3afalse%2c%22NumberOfAdults%22%3a1%2c%22NumberOfChildren%22%3a0%2c%22NumberOfInfants%22%3a0%2c%22OpenSearchPanel%22%3afalse%2c%22DrawerTitle%22%3anull%2c%22ShowFlexiFares%22%3afalse%2c%22RemainOnStep1%22%3afalse%2c%22ComponentSender%22%3a%22SearchPod2_%2fde%2f%22%2c%22CurrencyCode%22%3anull%2c%22PaymentTypeCode%22%3anull%7d; ej20SearchCookie=ej20Search_0=WAW|*BR|2018-11-15T00:00:00||1|0|0|False||0|2018-11-15 15:15:33Z; ej20RecentSearches=ej20RecentSearch_0=WAW|*BR|2018-11-15T00:00:00||1|0|0|False||0|2018-11-15 15:15:33Z; mmapi.store.p.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22uat%22%3A%221573830904395%7C%7B%5C%22Domain%5C%22%3A%5C%22de%5C%22%7D%22%2C%22pd%22%3A%221573830932553%7C%5C%22-493244901%7CBAAAAApVAwCwpaFv8BA6ZQABEQABQt87bJgBAJIGry8NS9ZI5WQdHQ1L1kgAAAAA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8ABkRpcmVjdAHwEAEAAAAAAAAAAABFsgEA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8AAAAAAAAAAUU%3D%5C%22%22%2C%22srv%22%3A%221573830932560%7C%5C%22fravwcgeu05%5C%22%22%7D%7D; mmapi.store.s.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D; akacd_TrueClarity_SC=1542899733~rv=86~id=2fc76111a7ae23d8a7949a7ab0bbe589; FunnelJourney=%7B%22CorrelationToken%22%3A%22E030C1D6-0A2E-8A71-ECE5-A093132E1ACC%22%2C%22PaymentType%22%3Anull%2C%22Origin%22%3A%22WAW%22%2C%22Destination%22%3A%22*BR%22%2C%22Outbound%22%3A%222018-11-15%22%2C%22Return%22%3Anull%2C%22Component%22%3A%22SearchPod2_%2Fde%2F%22%2C%22FlexiFares%22%3Afalse%2C%22Adults%22%3A1%2C%22Children%22%3A0%2C%22Infants%22%3A0%2C%22JourneyPairId%22%3A1%2C%22CarSearchQuery%22%3Anull%2C%22Pairs%22%3A%5B%5D%2C%22FunnelJourney%22%3A%22defaultwithoffers%22%2C%22UsingFixedJourney%22%3Afalse%2C%22OpenChangeSearch%22%3Afalse%2C%22DrawerTitle%22%3Anull%7D; eJRebookingSession=90919d6f-57c8-4f6d-90e2-1364012602e6; RBK-XSRF=9BB0DB439E46DF51559E4794479209F4B35E26A7; ejSessionExpiry=1542298529804.62; bm_sv=8A29DB60A6BA5E765E9A724949D38450~+9Wq71koSEryJ7NgJ5JEfjjls+BnI3FE1GZPzkaIpFZmGc/M4ArAn9OaoIIJBrNHZspMJ0xUOPfgtbPgvoMtBpwVZBOzPoLXKldwCErLoEH97csnU68ENB6iDez4jl1oiaGuXdQS5ug90X367iAhs0BE/JYh4VXp2zBn5bpnRAs=",
            'Accept-Encoding': "gzip, deflate, br",
            'X-RBK-XSRF': "9BB0DB439E46DF51559E4794479209F4B35E26A7",
            'Accept-Language': "de,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,la;q=0.5",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Referer': "https://www.easyjet.com/de/buy/flights?isOneWay=on&pid=www.easyjet.com",
            'X-Transaction-Id': "E030C1D6-004D-0C09-C9AC-EB71FA722835",
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            'ADRUM': "isAjax:true",
            'Cache-Control': "no-cache",
            'Postman-Token': "4ab05625-0d1d-4518-8b58-752f01005735"
        }
        r = requests.get(url="https://www.easyjet.com/ejavailability/api/v22/availability/query",
                         params=data,
                         headers=headers)
        logger.info("easyjet status code = " + str(r.status_code))
        if r.status_code == 200:
            json_response = json.loads(r.text)
            flights = json_response['AvailableFlights']
            for flight in flights:
                json_flight = {
                    "airportA": flight['DepartureIata'],
                    "airportB": flight['ArrivalIata'],
                    "airline": "EasyJet",
                    "dateDeparture": flight['LocalDepartureTime'].split('T')[0],
                    "dateArrival": flight['LocalArrivalTime'].split('T')[0],
                    "timeDeparture": flight['LocalDepartureTime'].split('T')[1],
                    "timeArrival": flight['LocalArrivalTime'].split('T')[1],
                    "number": flight['FlightNumber']
                }

                if flight['FlightFares'][0]['SeatsAvailable'] > 0:
                    flight_fares = flight['FlightFares']
                    json_fares = []
                    json_types = []
                    for flight_fare in flight_fares:
                        json_types.append(flight_fare['FareType'])
                        prices = flight_fare['Prices']

                        adult = prices['Adult']
                        json_fares.append({'amount': adult["Price"], 'currency': 'EUR'})

                    json_flight["types"] = json_types
                    json_flight["fares"] = json_fares
                    res_url = 'https://www.easyjet.com/en/buy/flights/' + depart \
                              + '/' + arrive + '/' + date_str + '//' + adults + \
                              '/' + teens + '/' + children + '/' + infants

                    json_flight["url"] = res_url
                    results.append(json_flight)
            return True
        return None
