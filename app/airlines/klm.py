import requests
import json

class KLMInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date, adults, children, infants):
        print("############  KLM ############")
        url = "https://www.klm.com/ams/search-web/api/initial-state"
        print(date)
        querystring = {"country": "UA", "language": "en", "localeStringDateTime": "en", "localeStringNumber": "ru"}

        payload = "{\"customerSelection\":{\"cabinClass\":\"ECONOMY\",\"selectedUpsellProduct\":null," \
                  "\"passengerCount\":{\"ADULT\":" + str(adults) + ",\"CHILD\":" + str(children) + ",\"INFANT\":" + str(
                   infants) + "},\"connections\":[{\"origin\"" \
                   ":{\"airport\":{\"code\":\"" + depart + "\"}},\"destination\":{\"airport\":{\"code\":\"" + arrive + "\"}}," \
                   "\"departureDate\":\"" + date +"\",\"outboundMonth\":\"\",\"fareFamilyCode\":null,\"" \
                   "selectedFlightProduct\":null,\"barVisible\":false},{\"origin\":{\"airport\":{\"code\":" \
                   "\"" + arrive + "\"}},\"destination\":{\"airport\":{\"code\":\"" + depart + "\"}},\"departureDate\":null," \
                   "\"outboundMonth\":false,\"fareFamilyCode\":null,\"selectedFlightProduct\":null," \
                   "\"barVisible\":false}],\"barVisible\":false,\"customerSelectionSet\":false}," \
                   "\"settings\":{\"maximumNumberOfSeats\":9,\"minimumNumberOfAdults\":1," \
                   "\"countrySwitchMandatory\":false,\"defaultAirport\":\"" + depart + "\",\"groupTravel\":false," \
                   "\"daysUntilLatestReturn\":359,\"showRatings\":false,\"upsellFbBenefits\":false," \
                   "\"dayFaresOffset\":6,\"monthFaresRange\":12,\"minMaxDaysOffset\":12,\"minDaysOffset\":4," \
                   "\"nextConnectionOffset\":7,\"highAccuracyThresholdPercentage\":92," \
                   "\"mediumAccuracyThresholdPercentage\":50,\"brandedFares\":[{\"codes\":[\"LIGHT\"," \
                   "\"SMART\",\"LIGHTNA\",\"LIGHTLH\",\"LIGHTONELH\",\"LIGHTSH\"],\"color\":\"#72c9f6\"}," \
                   "{\"codes\":[\"STANDARD\",\"FLEXLH\",\"STANDARDNA\",\"STANDLH\",\"STANDTWOLH\",\"STANDARDSH\"]," \
                   "\"color\":\"#00a1de\"},{\"codes\":[\"FLEX\",\"FULLFLEX\",\"FLEXNA\",\"FLEXFYNA\"," \
                   "\"FLEXTWOLH\",\"STANDPLH\",\"FLEXSH\"],\"color\":\"#007eae\"},{\"codes\":[\"DEFAULT\"]," \
                   "\"color\":\"#00a1de\"}],\"splitTaxes\":false,\"starRatingLink\":\"" \
                   "https://allratings.klm.com/#/{country}/{language}/{departureDate}/{departureDate}" \
                   "/{flightNumber}/allratings?starRating=true\",\"currentDate\":[2018,10,15]," \
                   "\"lastReturnDate\":[2019,10,9],\"locale\":{\"country\":\"UA\",\"language\":\"en\"," \
                   "\"localeStringDateTime\":\"en\",\"localeStringNumber\":\"ru\"},\"allowedOrigins\":" \
                   "[{\"code\":\"" + depart + "\",\"type\":\"airport\"}],\"legacySearchPath\":" \
                  "\"https://www.klm.com/travel/{country}_{language}/apps/ebt/calendar.htm\",\"customizeUrl\":" \
                  "\"https://www.klm.com/ams/ancillaries/customize/{conversationStateId}?application={application}" \
                  "&country={country}&lang={language}&rp={return_URL}\",\"checkoutUrl\":\"https://www.klm.com/ams/" \
                  "checkout-beta/ticket?backUrl={return_URL}&lang={language}&country={country}&frame=b2c#create-order" \
                  "?conversationStateId={conversationStateId}\",\"convergedSearchUrl\":\"https://www.klm.com/ams/lsi" \
                  "/endpoint/v1/deeplink?country={tld}&language={locale}&target=\",\"bamUrl\":\"https://www.klm.com/" \
                  "beacon/baminsights\",\"webUrl\":\"https://www.klm.com/ams/search-web/\",\"appVersion\":\"6.16.1\"," \
                  "\"captcha\":{\"enabled\":true,\"urlPattern\":\".*?/search-web/api/(flight-products|initial-state).*\"" \
                  ",\"strength\":1,\"separator\":\"-\"},\"barsEnabled\":true,\"applicationId\":\"EBT7\"},\"" \
                  "requestParameters\":{\"fares\":{},\"flights\":{}},\"translations\":{\"general\":{\"noFlightsFound\":" \
                  "\"Sorry, there are no flights available on this route or date. Please try a different airport or date. " \
                  "You can also contact the KLM Customer Contact Centre to make a booking.\"}},\"country\":\"UA\"," \
                  "\"language\":\"en\",\"localeStringDateTime\":\"en\",\"localeStringNumber\":\"ru\"}"

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "a80d5aea-95a9-4059-a874-1366944dde71"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        flights = response['flightList']
        print("!!!! KLM !!!!")
        print(response.text)