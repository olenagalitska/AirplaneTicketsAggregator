import scrapy


class Spiderman(scrapy.Spider):
    name = "spiderman"
    start_urls = [
        'https://en.wikipedia.org/wiki/Ukraine_International_Airlines',
        'https://en.wikipedia.org/wiki/Wizz_Air',
        'https://en.wikipedia.org/wiki/Ryanair',
    ]

    def parse(self, response):
        table = response.css("table.infobox.vcard")[0]
        caption = table.css("caption::text").extract_first()
        codes = table.css(".nickname::text")

        if (len(codes) == 4):
            del codes[1]

        info = table.css("tbody>tr")
        info = info[4:]

        result = """
            <br> 
            <h3> {0} </h3> <br> 
            
            <table> 
                <tr> 
                    <th> IATA </th>
                    <td> {1} </td>
                </tr>
                
                <tr> 
                    <th> ICAO </th>
                    <td> {2} </td>
                </tr>
                
                <tr> 
                    <th> Callsign </th>
                    <td> {3} </td>
                </tr>
            </table>
            
            <br>
                    
        """.format(caption, codes[0].extract(), codes[1].extract(), codes[2].extract())

        if info is not None:
            result += "<table>"
            for row in info:
                result += "<tr> <td> {0} </td> <td> {1} </td> </tr>".format(
                    row.css("th::text, th>a::text").extract_first(),
                    row.css("td::text, td>div::text, td>a::text").extract_first())
            result += "</table>"
        result += "<br> <hr>"

        filename = '../../../app/templates/airlines.html'
        with open(filename, 'a') as f:
            f.write(result)
