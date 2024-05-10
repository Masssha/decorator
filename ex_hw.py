import requests
from bs4 import BeautifulSoup as BS
from fake_headers import Headers
import json
from decor_hw_01 import logger


headers_g = Headers(os='win', browser='chrome')
vac_info = []
page = 0
@logger
def parcer_hh():
    for page in range(4):
        url_name = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}'
        response = requests.get(url_name, headers=headers_g.generate()).text
        soup = BS(response, features='lxml')
        all_vacans = soup.find('div', id='a11y-main-content')
        for vac in all_vacans:
            for vv in vac:
                v = vac.find('div', class_='vacancy-serp-item__layout')
                if v:
                    name_v = v.find('span', class_='serp-item__title-link serp-item__title')
                    place_v = (v.find_all('div', class_='bloko-text'))[-2].text
                    comp_name_v = v.find('div', class_='vacancy-serp-item__meta-info-company')
                    salary_v = v.find('span', class_='bloko-header-section-2')
                    link = v.find('a', class_='bloko-link')['href']

                    headers_gg = Headers(os='win', browser='chrome')
                    response_vac = requests.get(link, headers=headers_gg.generate()).text
                    soup_vac = BS(response_vac, features='lxml')
                    discr = soup_vac.find('div', class_='g-user-content')
                    if 'Django' or 'Flask' in discr.text:
                        if name_v:
                            vac_info_dic = {}
                            vac_info_dic[f'position'] = name_v.text
                            if comp_name_v:
                                vac_info_dic[f'company name'] = comp_name_v.text
                            vac_info_dic[f'company location'] = place_v
                            if salary_v:
                                vac_info_dic[f'salary'] = salary_v.text
                            vac_info_dic[f'link'] = link
                            vac_info.append(vac_info_dic)
        page = +1
    print(vac_info)
    print(len(vac_info))

    with open('vacancies_Django_Flask.json', 'w', encoding='UTF-8') as file:
        json.dump(vac_info, file, indent=5, ensure_ascii=False)

parcer_hh()