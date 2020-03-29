from Fetch_Data.database import DB
import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import Fetch_Data.fa2en
from persiantools.jdatetime import JalaliDate
import mysql.connector

db = DB()

# url = "https://bama.ir/car"

# get farsi to eng brands and models
# for brand in brands:
#     if brand['value'] == '': continue
#     eng_brand = brand['value'].split(',')[1]
#     link = "https://bama.ir/car/" + eng_brand
#     farsi_brand = brand.get_text()
#     brand_fa_2_en[farsi_brand] = eng_brand
#     while (True):
#         try:
#             session = HTMLSession()
#             r = session.get(link)
#             r.html.render()
#             break
#         except:
#             print("try again")
#             time.sleep(5)
#
#     soup = BeautifulSoup(r.html.html, 'lxml')
#     models = soup.select("#selectedTopModel")[0].find_all('option')
#     print(eng_brand)
#     for model in models:
#         if model['value'] == '': continue
#         eng_model = model['value'].split(',')[1].replace('-', ' ')
#         farsi_model = model.get_text()
#         model_fa_2_en[farsi_model] = eng_model

brand_fa_2_en = Fetch_Data.fa2en.get_brand_fa_2_en()
model_fa_2_en = Fetch_Data.fa2en.get_model_fa_2_en()

page_number = 0
counter = 1
ended = False

links = []

f = open('seen_links.log', 'a')
f.close()

f = open('seen_links.log', 'r')
lines = f.readlines()
for line in lines:
    line = line.replace("\n", "")
    links.append(line)
f.close()

model = ""
brand = ""
kilometers = ""
release_data = ""
cost = ""
body_status = ""

while (True):
    if page_number == 700: break
    if counter == 10000: break
    if ended: break
    page_number += 1
    print("Scraping in page: " + str(page_number) , "...")
    while True:
        try:
            url = "https://bama.ir/car/all-brands/all-models/all-trims?page=" + str(page_number)
            r = requests.get(url)
            break

        except requests.exceptions as err:
            print("Something went wrong: ", err)

    soup = BeautifulSoup(r.text, 'lxml')
    divisions = soup.select(".listdata")

    brands = soup.select("#selectedTopBrand")[0].find_all('option')
    link = ""
    for div in divisions:
        try:
            soup = BeautifulSoup(div.__str__(), 'lxml')

            # body status(color or no color)
            body_status = soup.select("#body-status")[0].get_text().replace("،", "").strip()
            if body_status != "بدون رنگ":
                continue

            # cost
            cost = soup.select('.cost')[0].get_text().replace(" ", "").replace(",", "").replace("تومان", "").strip()
            if cost == "توافقی" or cost == "حواله" or cost == "پیشفروش":
                continue
            else:
                try:
                    cost = int(cost)
                except:
                    break
            # link of car
            link = soup.select(".cartitle-desktop")[0]['href']
            if link in links:
                ended = True
                break

            # save link to file:
            f = open("seen_links.log", 'a')
            f.write(link + "\n")
            f.close()

            # release date
            release_data = soup.select(".year-label")[0].get_text().replace(" ", "").replace("،", "").strip()
            release_data = int(release_data)
            if release_data < 1800:
                date = JalaliDate(release_data, 1, 1).to_gregorian()
                release_data = int(date.year)

            # brand and model
            brand_and_model = soup.find_all("h2")[1].get_text().replace("، ", ",").strip().split(',')
            brand_fa = brand_and_model[0]
            model_fa = brand_and_model[1].split('،')[0].strip()
            brand = brand_fa_2_en[brand_fa]
            model = model_fa_2_en[model_fa]

            # kilometers
            kilometers = soup.select('.price')[1].get_text().replace(" ", "").replace("کارکرد", "").replace(",", "")
            if kilometers == "صفر" or kilometers == "-":
                kilometers = 0
            elif kilometers == "کارتکس":
                continue
            else:
                kilometers = int(kilometers)

            # save to database
            kilometers = str(kilometers)
            release_data = str(release_data)
            cost = str(cost)
            data = (brand, model, kilometers, release_data, cost)
            db.insert_to_table(data)

            counter += 1
        except:
            print(link)
            print(brand, model, kilometers, release_data, cost, body_status)
