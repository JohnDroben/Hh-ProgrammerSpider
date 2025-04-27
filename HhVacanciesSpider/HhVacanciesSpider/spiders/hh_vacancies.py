import scrapy


class HhProgrammerSpider(scrapy.Spider):
    name = 'hh_vacancies'
    allowed_domains = ['hh.ru']

    params = {
        'text': 'программист',
        'search_field': 'name',
        'area': 1,
        'per_page': 50
    }

    start_urls = [f'https://hh.ru/search/vacancy?text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+python&from=suggest_post&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'hh_vacancies.csv',
        'FEED_EXPORT_FIELDS': ['title', 'company', 'location', 'salary', 'link'],
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Chrome/91.0.4472.124'
    }

    def parse(self, response):
        for vacancy in response.css('div.serp-item'):
            yield {
                'title': vacancy.css('a.serp-item__title::text').get().strip(),
                'company': vacancy.css('a[data-qa="vacancy-serp__vacancy-employer"]::text').get('Нет данных').strip(),
                'location': vacancy.css('div[data-qa="vacancy-serp__vacancy-address"]::text').get('Нет данных').strip(),
                'salary': ' '.join(
                    vacancy.css('span[data-qa="vacancy-serp__vacancy-compensation"] ::text').getall()).replace('\xa0',
                                                                                                               ' ') if vacancy.css(
                    'span[data-qa="vacancy-serp__vacancy-compensation"]') else 'Не указана',
                'link': vacancy.css('a.serp-item__title::attr(href)').get().split('?')[0]
            }

            # Обработка пагинации
            next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
