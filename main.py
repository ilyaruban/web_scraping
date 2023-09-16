import bs4
import requests
import json

with open('data.json', 'w', encoding='utf-8') as data_json:
  url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0'
  headers = {
    'Host': 'hh.ru',
    'User-Agent': 'YandexBrowser',
    'Accept': '*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection': 'keep-alive'
  }
  responce = requests.get(url, headers = headers)
  html_data = responce.text
  soup = bs4.BeautifulSoup(html_data, features='lxml')
  div_tag = soup.find_all('div', class_='serp-item')
  for i in div_tag:
    if 'django' in i.find('a').text.lower() or 'flask' in i.find('a').text.lower():
      city = i.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy-address'}).text
      href = i.find('a').get('href')
      name = i.find('a').text
      salary = i.find('span', class_='bloko-header-section-2')
      company_name = i.find('div', class_='bloko-text').text
      if salary is not None:
        salary = i.find('span', class_='bloko-header-section-2').text
        salary_str = str(salary)
        json_data = {
          'link': href,
          'vacancy_name': name,
          'salary': salary_str,
          'company_name': company_name,
          'city': city
        }
        result = json.dumps(json_data, ensure_ascii=False, indent = 4)
        data_json.write(result)