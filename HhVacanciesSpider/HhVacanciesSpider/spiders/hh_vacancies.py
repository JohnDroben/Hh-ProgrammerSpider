import scrapy
import  pandas as pd
from urllib.parse import urlencode
from scrapy.exceptions import CloseSpider

class HhProgrammerSpider(scrapy.Spider):
    name = 'hh_vacancies'
    allowed_domains = ['hh.ru']

    params = {
        'text': 'программист',
        'search_field': 'name',
        'area': 1,
        'per_page': 50
    }

    start_urls = [f'https://hh.ru/search/vacancy?{urlencode(params)}']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'hh_vacancies.csv',
        'FEED_EXPORT_FIELDS': ['title', 'company', 'location', 'salary', 'link'],
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Chrome/91.0.4472.124'
    }

    def parse(self, response):
        if "captcha" in response.url:
            raise CloseSpider("Обнаружена капча! Прерываю работу.")

    def parse(self, response):
        for vacancy in response.css('div.serp-item'):
            yield {
                'title': vacancy.css('h2.bloko-header-section-2::text').get().strip(),
                'company': vacancy.css('a.magritte-link___b4rEM::text').get('Нет данных').strip(),
                'location': vacancy.css('span.vacancy-serp__vacancy-addres::text').get('Нет данных').strip(),
                'salary': ' '.join(
                    vacancy.css('span.magritte-text___pbpft_3-0-32::text').getall()).replace('\xa0',
                                                                                                               ' ') if vacancy.css(
                    'span.magritte-text___pbpft_3-0-32') else 'Не указана',
                'link': vacancy.css('a.a.bloko-link::attr(href)').get().split('?')[0]
            }

            # Обработка пагинации
            next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

            # Обработка детальной информации о вакансии
            yield response.follow(response.css('a.serp-item__title::attr(href)').get(), callback=self.parse_vacancy)

    def parse_vacancy(self, response):
        yield {
            'description': response.css('div.vacancy-description').get().strip(),
            'requirements': response.css('div.vacancy-requirements').get().strip(),
            'benefits': response.css('div.vacancy-benefits').get().strip(),
        }
        df = pd.read_csv('hh_vacancies.csv')
        print(df)


