import scrapy
from utils.get_tokens import get_tokens
url = 'https://divar.ir/v/-/{post_token}'
cities = {
    'tehran': 1,
    'mashhad': 3,
    'isfahan': 4,
    'tabriz': 5,
    'shiraz': 6,
}


class HousePostsSpider(scrapy.Spider):
    name = 'divar-light-house'

    start_urls = [url.format(post_token=token) for token in get_tokens(last_post_date=1680787229082899,
                                                                       city_number=cities['tehran'],
                                                                       n_pages=21,
                                                                       post_category='house-villa-sell')]

    def parse(self, response, **kwargs):
        informations = response.css('div span.kt-group-row-item__value::text')

        area = int(informations[0].extract())
        construction = int(informations[1].extract())

        address = response.css('div div.kt-page-title__subtitle--responsive-sized::text').extract()
        price = response.css('div p.kt-unexpandable-row__value::text').extract_first()

        description = response.css('div p.kt-description-row__text--primary').extract_first()

        yield {
            'area': area,
            'year': construction,
            'address': address,
            'price': price,
            'description': description
        }