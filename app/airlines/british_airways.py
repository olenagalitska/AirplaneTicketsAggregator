import requests
import json
from app import logger


class BritishAirwaysInfoRobber:
    @staticmethod
    def get_flights(results, depart, arrive, date, adults, children, infants, teens):
        logger.info('in method')
        logger.debug(
            'depart: ' + str(depart) + '; arrive: ' + str(arrive) + '; date: ' + str(date) + '; adults: ' + str(
                adults) + '; children: ' + str(children) + '; infants: ' + str(infants) + '; teens: ' + str(teens))

        # url = "https://www.britishairways.com/api/sc4/badotcomadapter-paa/rs/v1/flights/fares;calendarDays=3;cabins=Economy;ticketFlexibility=RESTRICTED;maxPointsEarningFare=false;language=EN;includeCalendar=true;"

        # data = {
        #     "locale": "en_UA",
        #     "inboundDestination": depart,
        #     "inboundOrigin": arrive,
        #     "outboundOrigin": depart,
        #     "outboundDestination": arrive,
        #     "outboundDate": date,
        #     "adultCount": adults,
        #     "youthCount": 0,
        #     "childCount": 0,
        #     "infantCount": 0
        # }

        # headers = {
        #     'Authorization': "Bearer 196e5f1376ff02051954a84a7fc501bd",
        #     'ba_client_applicationName': "ba.com",
        #     'X-MjuOycaA-a': "wUggTGasp9H8Lnk7zMZxTAYyCtrd9Vkq9ddtHuvNwTcnjDZC4q57awgD9VoriYgzwvdDnqIMx9r_4AV_TqSTLq50j5ZXHqB2d28vHqs8jqSbTUnEE6EIao_cER9DbqfmHIv7X-5sutmdeAubwFVVU4gvwsnKLqyVaEy_N5l0jDkVbejNwFub1lZZaAVdiYe8wqIb1QdWaqoCrYd6wCPpuN8tHdoxE7cO=DdXb2i0PxdGYOdCTsnsoAg0_NKn9QbNwvE=T6dW1UvNTGe0wGdCH5BNa4ZmoPEvHI9WpqVUn0S_LboTa7n-HPNfPRE=iRkjoOd-ixs=v-rzzIyTT_odQqzvECHGaFSdz2dvneU0oPrOiuHzLPjwPRnZkbN7Ov8xwS_mSF5Zk2osy6k71EH8jqfNj=dCTPo5V-jXiRgW-RosHDZX6DjN1O=jVjo2FMTN9Us8uU97wxbNsWns4DrNODoDw0S51UyCTq_snIsFnVnxksNvaP8xjqStHqnbwDjlaunvaA5sz5n7jIuNixd=IqV5Hr_C1ASsaOsmLMZbvFn_TAyG4A9snwg-iYyxixSWiEkR1frnLDojjb2vn5SSkxs3a=bKHDoz5AsOTqvWbqwNaU9WOU9szusti6nsoPonTpDdHWZCkWNNzFuXTFPpHrnTvY2_4f2UX3kNoA_D9UlZq2wNgU9TiPdzwFyZibK_Tbd3CA9YiUaExFIVLbI7nMaG1mntv=dZH2Dgi=s5kVSuHD3sk=ds1FoZEMZsuTXNHM6XeIjLrC-4MmG0Iqvb4U574O_cQYdDomTX9PgswYn-H=d7Hoa8jquNa7Y6Cu92b29CwCPvPCr7yF9xHUl0w3r0bqYvwMnWHpjyPCseTqZsADuNm9SWTE2ZyF9vHAsZzAwLa2STQdZszA9Ci-bkK2aZQbd04mN7P7dCHUPzqnXbHq9YCVSVAqkN5YHZkCHXg3gCb2oZaUu8Hq4NaPIvPUnXwB5xiu70oRE=1QgWnA_8T4gDHqC6X0dv1_yWTw5cpR00i0S9nUsWeOs5Dfg-HDdWPRkzwPnXrUS7bddvisr0TE5euxGZ9_VsnFS2H4d-Px2FvGbXePgDa=zNL25-HEw8XFHsCRsmoAnu8F5Gj2mdXI7ziFICi9B-TNIlw2X7PfjtOCVcuUc5dUVCTvIRQE5Zj5o9HprZ92dX9qSDjqBCzRdsXYy-aAuN4VSGwY2v1AyCwxdz9pVs4mdWaqZm1u2ZiULsPUs8aDoZTAosBIdx_q_xRHZunq_Uv2nXTqScvFk-uVSmrBsVL4_vaObNP7ZKaO_gowHZkAu-bFoWkpgz4ogbX0ZmaFHWEboZT5SPJ25pv8YyTvdCdqoQeE5bvsoYTC9ZiYSZj=N9n4S=a6EiwxBbT0dsXscxwRnPUqa7HxzMa0dsxtZYjIdsHMYevKJ_195taI9yw3gGqFnRPU5POCx0QAJGnVl=dqI-oOdsw-a6aQqIPVoG-C7joAuLwDnV9qVZT5Bedp00bT80ixb=9O2NEGZWXIsqkYynEUsZHqs8P7iv411bExdx4=Z7zY9xTOa_9UovwsnvoI59HF9jPUBviUScoLb-BqV8iR2Z1Rn-i2kvi9S8C0dsv6gToUEjj2TiTU5t4PgclFPN4q9mjen0fN=0qb2FkuCUiu5maObU1A9CjIds9xdCj=ds1ETeaUrdk5Hv5x_C1PgWzqyGiGasHqB-Hbdxi6ocXpd0iVSZP7g0aEDNOA9ZiqotwUv-kq9m14dVz0bXxA1IAb5zjq_Ew6otjIqbvYgsHqZ7Eq_s1C5CwFFIk7oueq5snSHza6k2H6gZaI7zdIWjDP9sTqn=TpdW2RnxiVStau_9LqyEO-yVawwNbqCNT5lziF98Tq9ruU9FX6EsPRo-Pv5s1U_m1L55TBaDHDg8LDZZ9fb7aAsZPCHxRPn25UXxTwssiUSCePG6yF_CHTHCXFJNkUS-wFJ7zEuNExb8HFyWwRgxHA58itZ3jTYdoqVvjpo_aAyOwFy7HQdXiPgGux2ZFkoQEAVWiI9myLgWHRg7r0b-H=ssA5SX95BRnASZTc_71A_MwU9Gj2nmkBssOUuNH=SZwYV2ouuN9CwbbqsX1OdGHDoOzp5saOSKYRuNjDgG7q9vyFI7dFs-97dsbqwyvYSxOABAP7PxjDosnxdZHA9CjMZZw6u7TPg0XWseaYsm1xdtwxdZjDE_ax_si7cJwF-LWPomxRd8iCy1rCzdjTINwUZViFo-wFS7ETZ5iRE=CA6FHegGL590wZuI1GT=aH1y1Gdl5Rog1AINvUnsnPoziSa9O8s51Ens0YH7pIy01uICf3gteA5z9U9taFgZ7EnEzGg-BBIkNq57H2DZ0PgUTFP=ana-w6g6PRnPH4bW8RPZUsHtAq9GIR9C4TcsaPbXLInUU2ZDHDr=PU5GwquVe2uvjDa_PUk-jDoskxdVa0dCHATvTDgx9=bNjquxbDoZdw5-4Tizwv8maPbRiCV51AVsjq_siU75nbdFH=2vi5BvTRgZLd5GaAxtQqs-kP=N1G0tH5SZ14guaPg8xFub4Gm3kqsPB=J7yUa5OUg-oRg-49llXp1-oPj6u7gWop50HuxXfAnmaxdsBRg2ERomXDoXHAymiIt6r3TU19S-wWZC9UM14AIIw5H-p=_CiRgcwq7ZiAI71fgVauBR4C2Yntr7aUNWrU9eaFsmXsr3rsSFb29uiE55EPos9Dg-qPjWwRuVPBZ-xMMbzUSgaqg-nkd-129m4PsGHQjROP9V3AHYjDoFEu5sHk8WksS0wFVz1GTNHIH59qsm4kZVEIRjasoGqIbvix2zTAymuFJliVSYaEd1Tu9-amsUj=dI9qyCiLgCHDgsTA5xa6gsakX8wFs-eDotwF9719nMw=2un9lzPRoFLunuzZ_Gw6otu6Y8wI7eiVSWaWZYH5g-TqvXwFgcwWZ71CgxPU57w6EqbqssbquNwFcvAIjxOwgYb=dmHISxzIyGrG9FXtgx16kW1UcIXGIRk0bNH2NeCCuNaPoGuCkBE2jxQwgY9DnWHAybomd-iso5X0_6TtN7aujNaDTxaY9Gd25CH2jCQOdMEAPr1tr0e=yxHmZsnco9EqBWj5Ssi5bda=SGaLocaPnVaqIGiU9sTmZDuFRaCPjv9GsWwNouTqDZH5HWExtVoALG9I9VPRH-vFs-kqsVPLnTw0B3r8s8wGbNCq_Zi6YUaOdTvD9PLqa7iB9xPxdDlCs57vjbwCvyPvdCiAcEiUgCi697zFoDL9dYaPgxuZo=oQg9H=dZE=bNA=2daAD_H45siUIboHoWbDr0aVTzjq9xwGnZaEeaTRoCx-dT1o9xP7Ybiq9veiy5iDZCOmZtjqNXwx63",
        #     'X-MjuOycaA-b': "2cqyv1",
        #     'X-MjuOycaA-c': "AMBrkBdnAQAAUGbZG08OK_xYs0S5KNWwHXG6ZSBdPkXg7Levdn2-j9E0W567",
        #     'X-MjuOycaA-d': "0",
        #     'X-MjuOycaA-uniqueStateKey': "A_y5lhdnAQAABPcUO95ri4_BjDhSe6W3r8szyNjjcoHbpkKnY1Kj9gNdBD79AawUGfGucvDHwH8AAOfvAAAAAA==",
        #     'Cache-Control': "no-cache",
        #     'Postman-Token': "3b8d7f5a-c6ce-46c3-9def-fecdd5340b1b"
        # }

        url = "https://www.britishairways.com/api/sc4/badotcomadapter-paa/rs/v1/flights/fares;outboundOrigin=KBP;outboundDestination=FRA;outboundDate=2018-11-30;calendarDays=3;adultCount=1;youthCount=0;childCount=0;infantCount=0;cabins=Economy;ticketFlexibility=RESTRICTED;maxPointsEarningFare=false;language=EN;includeCalendar=true;"

        data = {"locale": "en_UA", "inboundDestination": "KBP", "inboundOrigin": "FRA"}

        headers = {
            'DNT': "1",
            'Accept-Encoding': "gzip, deflate, br",
            'ba_api_context': "https://www.britishairways.com/api/sc4",
            'Accept-Language': "EN",
            'Authorization': "Bearer 57384556e771dd7d883b850dff13f0de",
            'Cookie': "BIGipServerba.com-port81=1131980451.20736.0000; v1st=9ED8B105E8D8E2FC; TS01d61f40=01067462077c26f631080886a296abd80530432f326f1fc2e520893613cc4c7365f7cd0ad41b4bb703dfe7359953dbace927ea0d9851b8bcdec898a75345b7ceb6c5143d0402b2414e82991aedff8ab89e1c314bb593c48bdacb81aac4691c9c8bc87515d8; BA_SITE_PREF=full; mmapi.p.srv=%22fravwcgeu11%22; BIGipServersolr-live.baplc.com-80=544777891.20480.0000; RSR_RESULTS=empty; BIGipServersolr-live.baplc.com-81=544777891.20736.0000; Allow_BA_Cookies=accepted; Allow_BA_Cookies_Date=Thu Nov 15 2018 13:34:08 GMT+0200 (Eastern European Standard Time); betaReferrer=https://ru.wikipedia.org/; BA_COUNTRY_CHOICE_COOKIE=UA; BA_LANGUAGE_CHOICE_COOKIE=EN; ba_client_sessionId=dd304528-2240-4338-bdbb-fb0817f700b5; betaUser=62; retDate=; _cc=AckxJgVe3xHpp/sHT+7sSpus; JSESSIONID=6885A8E2BFF1F5EEAC12EA41A4B694BD.iwls-live-left2a; BIGipServerba.com-livesite.ba.com-port81=561686179.20736.0000; FS_DEPT_COUNTRY=UA; mmapi.p.uat=%7B%22FSRequestedHaul%22%3A%22FlightSH%22%2C%22FSRequestCabin%22%3A%22M%22%2C%22FSRequTcktType%22%3A%22Restricted%22%7D; mm_maxdiscover=1; AKA_A2=A; publicAccessToken=57384556e771dd7d883b850dff13f0de; publicRefreshToken=0c42b9408625edebe46f99225428b98a; BASessionA=GLvTbtYf38CkX41y0tKlmRVZgJ22ptG9txTkGvp25ZQG6g7HHMr1!-165074437!blx42al01-wl01.baplc.com!7001!-1!-1929120160!blx43al01-wl01.baplc.com!7001!-1; BAAUTHKEY=675a8628-1227-4049-b52d-aa97ebf84017; TS013c27e3=010674620792c0907ac61e22ee3f4800d98141210e0b6043a4dde1527130321b67465bff4caadba48ad87326a39de7f20c6b3085bbe6655100fb978c82ddfc45926d6fd21633f8adc7c8f707670ec3faf0c4c2d50969ebfeaa7a8c6e8110dad6ed20763b7d2f3144336a1073f3b1fd3c7594e667d059ffa1db62351fdfb9df09b8979c7c208329bee12d04b8cf0b6b27c3a9fbcdc3b0a60ce135326cb423ab73b32203dbfb; dtCookie=A6E7AF970D349974C053C2D23C3CE11F|QnJpdGlzaCtBaXJ3YXlzK3dlYnNpdGV8MQ; dtSa=-; dtLatC=7; mmapi.p.tst=0.004; mmapi.p.pd=%221688442536%7CGAAAAApVAwAZqkGn8BD%2FgwABEQABQtm9PfsEACKKIbcTS9ZIs%2FS7Pu5K1kgAAAAA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8AFnd3dy5icml0aXNoYWlyd2F5cy5jb20C8BAEAAAAAAAAAAAA6HYBAOh2AQDodgEAAAAAAAAAAAFF%22; FS_DEPT_AIRPORT=KBP; depDate=30%2F11%2F18; FO_DESTINATION_COOKIE=Frankfurt%2C%20Frankfurt%20(FRA)%2C%20Germany%7C1543528800%7C979855200%7COWFLT%7CEconomy%7CLOWEST; dtPC=297736251_686h20",
            'Connection': "keep-alive",
            'ba_client_sessionId': "dd304528-2240-4338-bdbb-fb0817f700b5",
            'X-MjuOycaA-c': "AADAGRhnAQAAIPVViDK9UDmPM_D2SdIckFtItdN49uYU9AMT-Corvx3TUkSm",
            'ba_client_deviceType': "DESKTOP",
            'X-MjuOycaA-uniqueStateKey': "AzbUGxhnAQAAfsB5uc34Ruw86e_7dJULEAEV8sTDAKCFtgXNGjXHgz-cbJ_gAawUGfCucvDHwH8AAOfvAAAAAA==",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            'X-MjuOycaA-d': "0",
            'Accept': "application/json,  application/javascript",
            'ba_client_applicationName': "ba.com",
            'X-MjuOycaA-a': "j1t7yQXVmXrwhn-rdMg53aADf7sqdr1fUNR-X19m6LjtKtdNYN2dbSV12y1fUtR9xBUVrAVv6mj9mb0JLok4dN91MvhqGmyPptyw030v2c9qGmgtUobqhP280p8F2Q-OY_q0jogW32kwXYywdNb-BmtWG8SAi=VDUNgEiBgOCQb3My99b=8cd=CfbNUI0C-N_Y1-Q7HAIos3VNb9xNgxyoEwRKtSHM83aO80UN89KC=HiBb9h8jtep8Hi7UzUoyQ6vjARyqEjOg9UNUwV=MS6E9EyBg1dAg5byUbhot-LtU6hOpn6Ks5UNeYLK3oRxcSiNR9hok10KzEf=SGdosE357V9=hwtmwQivs4bC8pV7g5V5-gqEvvdo-qLN0Jd=zJGmkK3Q82GKtxbQg04n=FhB89THg3_rUVd3yDZtSnNoz7iw8Ed0w6hmf60ty4gQjFhHj7MQ=Px79I3oj-jN6qTETD0MR-zKjE2OR48PSwjmGq3bhwiK91G3t1GKfMLof0ir9xYKbv_S993mjxSORm6KTV6bj1SoyqU071twtEUtedG=hEhPUwMHBn4TzA0KdQi=0wTHt7EMGJXvyVDKb83pftVob9jOgc3bs7ZNOwx3tEKNw4GK7cebyvV0gW6KRc6KbcjxVwp1=SdSD46KfTobgEpvdmL30qxog0dMg5UthVh481GK68erz5eos-Uj8=VtdIUtT46R-FUrbxi1R-G1jbiS8Th9ycp_NwzwIxdSV1d8R1RM8E_tsW3dq9tms-jK9FLr4IYMj0637a13XziHsF3ofE2mvWhHyXxQC2Em1SdMVQ6fxwhuFV4n-5itRFoQ8tUNR90MXwpMj0VFUw2mtQMxfFy1N1vn8AMHEzdEgxhn8DhHvq_7Uq0Bg5iBg9VS8-VmXxYoTwGYz-XP8JDob50741YmjNGTTzHNR9YtcSVNZ5REg=49stTHtNiN-Eebh1UNpnYMjFj3R3dS9m6MjEiEzMeKqTYSVwjtyOMH95610VVoRJdMgqimsTLoaZ4TsEdMbmM46wiN8=iE4wY3jM1bRcdNwEMDREGMgnbtCwGK9xd3Gxi=5364--LNhJGoYrRR8FGKj5hx9-hAjDia9xdozWYTfCYNbMdo4x6M376M8Cdmtx27R50e2jj0GDIS97xh2DiHd9UoLnImhD61C1boq-6HZeUozDwo010NgxSnSW6KywimNT0S89hHDcityzde8xdKz9Ug9nxoCIhtbcIn8B6Hb9hoMVUozEbos3hv2UUtREBp8x3MiSpNb5dp8cdS=PGMtq2JGmRHs901z5M1_wZoRxxHf-GpV1QKRM4wIJMEbthSkwiNR9ImyzvNg-ppVwpTzJiT51VosJxNg=doftiHfJEmi3im9qhH9cYdfjU=t7XsRtY1fAhOR4GMg5yHrzH3C8ZPgTjHrU4_rJdKj-61bNpp8cxmUE0x9mGbCS6QR2GKMajAGA_rbuh0gJjTMDGV8-hQ=ehHxAiHMRG0d9d0GqRHC1X1=NUC89hmMVh9LnGvagL=XIjC8D0KgSqoRT3SB3GhT4IOb90HGtiAuUGd-AiObNhH4DYhgtG10wiA0xM1VzU=tEhoNDdS8FiNRSSoMfbKq4_K99ibyQ6MXzhvywYdq9YotxUNgWMHg54o9AUoy8iZju0M0FMHTw3OvFVp8Wia0IbsG-b389630_63UIimbJtQREYMR-4mzJiOT1Uowxdof1hEv0TOgvXQg-doFqipVxd8bESnGFGKdq4QRqZTdNhNRqMHTwUotxiofciw89jTz5dKyB6w84M48N_MUwRMUwiObv49jEdrECUZ062E0wdrzIporEUob53SVQTHs9Ur0wTOX=Xr286Kz163VxhOg5LKtfRMRDzQR9X7bIGS89EKbZh1VwiMRt3S8Eimt4M18cdKsDGKdFhosAiQgti9a4_o4idK-7RE9EhmbqzB8JRHdc6mf9irFwImL-gH99UC9AVf7V09VwSFg5HS876m2m6n8-p7C13NR-_=t9YQ3W2J6VIC99gHDJ67gEUVI83=9VDrbFXA8c6YgciNUwhOGfd5-06Kt7RrW2dK-qjAKndoTCiBVzdSV5MHt7iKtpG_t7vKb9I9s3GK7w0S89Dbbc-S=S059OYNjvYKTxIOUwi3hJRKg5VojAT7WtVV81UN99YQU4RMgniovOhNgrd0dx3OjnhmXv0rz9UNgJZrzxVoTq6bw40x8J6mbEGpVxbKonXtVxUrspin-5hAtMihf-zmtc3vsvIn-vYM3Do7h4hFgMbowOhOXwKovEMH9vhn9xYTgcdKs-0S8E_ohHMHz8DS-54baShNgNUobqUoT48T8Evmj-hmTzUoDJYbs3Uoj0UVpnimg-0msMGOVwLtG9GKfChEbJaQTwiwvtUSk-GTbJGMg93aG-hAttGX89_KE4GV8ctof5e8k8eZRcGmG9MHbWHSVzYMgqjrzxccg9DwS1t3T4iBgNiQR9GKbE20wciHdn0V8TUoREdjXHZEgcjAGxML-E0oR9iBgp66mL=1bTbQjcYKbnGhgf2OVk3EMATmW7Gbf-_KrviKb9UB8JUNRAiEbJjrz1jnfudVXVjHbchm0SppfJiLNPGN3DHx8vGMR9Tz=UNMXJKobx69pweTonhyqqaEiDhc9j_rj50egJ6Qe9ixsN0Qg9U=t9d5-9ex=MiM85h7tEk=pw6KG1GKzpYKbN0vgNd=2NeY=80Cj-wovnh1jCb8-bV=MeiHz5RE=4ivs9GMjAiMd50mFQhc-cSAXV6bsxVowsYrbtGKrVhAg=hZG1Y8A7Mvs9dbsCG=fv6b-6bQTxEJGWjQjmdtsA6MRSpb3HGHjByNRMhofJiKRVeoTchwtmG68mhO956FN4MygEImtFirbW_ofxT1jmGKsNCmbJ6M-5RK-xU=t2in8kK=bViMj9bHjAx9bcdtXwVtd1dos5MHbJiHJVYHNOEH9JPTT4RK0QrNgqi13D_KGWIF88eo6X0I64dmsE6Ez-GQ24pvsxGTbEdtsxGKv9ZZtbix8047jIMQMDeVqNG5-EUVqCh1jAGKq7hn=rRbREV=grrX",
            'Referer': "https://www.britishairways.com/travel/booking/public/en_ua/",
            'ba_client_organisation': "BA",
            'X-MjuOycaA-b': "hzeq8n",
            'Cache-Control': "no-cache",
            'Postman-Token': "75d00dc8-bd3b-4769-bd55-070af56be268"
        }

        response = requests.request("GET", url, headers=headers, params=data)

        print(response.text)

        logger.info("british_airways status code = " + str(response.status_code))

        if response.status_code == 200:
            logger.debug("british airways, status = 200")
            json_response = json.loads(response.text)
            flights = json_response['flights']

            for flight in flights:
                logger.debug("in for loop")
                time_depart = flight['departs']
                time_arrive = flight['arrives']
                json_flight = {
                    "airportA": depart,
                    "airportB": arrive,
                    "airline": 'British Airways',
                    "dateDeparture": time_depart.split('T')[0],
                    "dateArrival": time_arrive.split('T')[0],
                    "timeDeparture": time_depart.split('T')[1],
                    "timeArrival": time_arrive.split('T')[1],
                    # "number": "0"
                }

                # segments -> code (it will be number of flight)

                cabins = flight['cabins']
                json_fares = []
                json_types = []
                for cabin in cabins:
                    fares = cabin['fares']
                    fare_and_curr = dict()
                    fare_and_curr["amount"] = fares[0]['fare']
                    fare_and_curr["currencyCode"] = 'USD'
                    json_fares.append(fare_and_curr)
                    json_types.append(cabin['type'])

                json_flight["types"] = json_types
                json_flight["fares"] = json_fares

                # res_url = 'https://www.ryanair.com/gb/en/booking/home/' + depart \
                #           + '/' + arrive + '/' + date + '//' + adults + \
                #           '/' + teens + '/' + children + '/' + infants

                res_url = "https://www.britishairways.com/travel/booking/public/en_ua/#/flightList?origin=" + depart + "&destination=" + arrive + "&outboundDate=" + date + "&adultCount=" + adults + "&youngAdultCount=" + teens + "&childCount=" + children + "&infantCount=" + infants + "&cabin=M&ticketFlexibility=LOWEST&journeyType=OWFLT"

                json_flight["url"] = res_url
                results.append(json_flight)

            logger.debug(results)
            return True
        return None
