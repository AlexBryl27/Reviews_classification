import requests
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver

driver = webdriver.Chrome('C:\chromedriver.exe')
films_list = []

for i in range(1, 7):
    driver.get('https://www.kinopoisk.ru/top/lists/223/filtr/all/sort/order/perpage/200/page/{}'.format(i))
    text = BeautifulSoup(driver.page_source, 'html5lib')
    films_list.append(text.select('tr[class="js-film-list-item"]'))

id_list = []
for x in films_list:
    for y in x:
        id_list.append(y['id'])

id_list = list(map(lambda x: int(re.sub('tr_', '', x)), id_list))

with open("id_list.txt", "w") as write_file:
    write_file.writelines(str(id_list))

def get_reviews(page, data):
    
    reviews = page.select('div[class="reviewItem userReview"]')
    for review in reviews:
        category_mark = review.find(itemprop="reviews")['class']
        if len(category_mark) > 1:
            category = category_mark[1]
        else:
            category = 'neutral'
        review_text = review.find(itemprop="reviewBody").text
        review_text = review_text.replace('\r', '').replace('\n', ' ').replace('\xa0', ' ')    
        
        if len(data[category]) < 1000:
            data[category].append(review_text)        
            
    return data

            
def parse_reviews(id_list):
    
    data = {'good': [], 'bad': [], 'neutral': []}
    i = 0
    while any([len(_) < 1000 for _ in data.values()]) and i < len(id_list):
        j = id_list[i]
        driver.get("https://www.kinopoisk.ru/film/{}/reviews/ord/rating/status/all/perpage/200/".format(j))
        page = BeautifulSoup(driver.page_source, 'html5lib')
    
        get_reviews(page, data)
        
        page_links = page.select('li[class="arr"]')
        if page_links:
            last_link = page_links[-1].a.get('href')
            num_pages = int(re.findall(r'/page/(\d{1,3})/', last_link)[0])
        
            for k in range(2, num_pages+1):
                driver.get("https://www.kinopoisk.ru/film/{}/reviews/ord/rating/status/all/perpage/200/page/{}/"\
                                       .format(j, k))
                page = BeautifulSoup(driver.page_source, 'html5lib')
                get_reviews(page, data)
            
        i += 1
    
    with open("reviews_data.json", "w") as write_file:
        json.dump(data, write_file)
    
    driver.close()
    return data, i

reviews_data, i = parse_reviews(id_list)