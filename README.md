# Hh-ProgrammerSpider
# Парсер вакансий программистов с HH.ru 

Сбор вакансий для разработчиков с hh.ru. Экспорт в CSV с фильтрацией по Москве.

## 📋 Особенности
- Параметры поиска:
  - Только названия вакансий
  - Регион: Москва
  - 50 вакансий на странице
- Сбор: должность, компания, локация, зарплата и ссылка
- Автоматический обход страниц

## ⚙️ Требования
- Python 3.13
- Scrapy 2.11+
- Pandas (для анализа данных)

## 🛠 Установка
```bash
git clone https://github.com/JohnDroben/Hh-ProgrammerSpider.git
cd JohnDroben/Hh-ProgrammerSpider
pip install -r requirements.txt

🚀 Запуск
bash
scrapy crawl hh_vacansies -O hh_vacancies.csv
Пример данных:

csv
title,company,location,salary,link
"Python Developer","ООО Техностарт",Москва,"от 150 000 ₽",https://hh.ru/vacancy/123

🔍 Анализ данных
python
import pandas as pd
df = pd.read_csv('vacancies.csv')
print(df['company'].value_counts().head(10))

⚠️ Важно
Используйте VPN при частых запросах

Соблюдайте условия использования API HH.ru

Зарплата может быть указана в разных валютах
