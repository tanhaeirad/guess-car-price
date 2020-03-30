from Fetch_Data.database import DB
from sklearn import tree
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time


def predict(brand, model, kilometers, year):
    db = DB()
    results = db.select(brand, model)
    x = []
    y = []
    for res in results:
        x1 = res[2]
        x2 = res[3]
        x.append([x1, x2])
        y.append(res[4])

    if len(x) == 0: return -1

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)

    new_data = [[kilometers, year]]
    answer = clf.predict(new_data)
    return int(answer[0])


def get_brands():
    url = "https://bama.ir/car"
    while True:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            break
        except requests.exceptions as error:
            print(error)

    array = soup.select("#selectedTopBrand")[0].find_all('option')
    brands = []
    for brand in array:
        if brand['value'] == '': continue
        eng_brand = brand['value'].split(',')[1]
        brands.append(eng_brand)
    return brands


def get_models(brand):
    url = "https://bama.ir/car/" + brand

    while True:
        try:
            session = HTMLSession()
            r = session.get(url)
            r.html.render()
            break
        except:
            time.sleep(2)

    soup = BeautifulSoup(r.html.html, 'lxml')
    array = soup.select("#selectedTopModel")[0].find_all('option')
    models = []
    for model in array:
        if model['value'] == '': continue
        eng_model = model['value'].split(',')[1].replace('-', ' ')
        models.append(eng_model)
    return models
