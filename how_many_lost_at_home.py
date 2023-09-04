from bs4 import BeautifulSoup
import requests as r
import datetime
from lxml import etree

# GET THE PAGE

today = datetime.date.today()

year = today.year

month = today.month

first_season_yr= 1992

last_season_yr = year + 1 if month >= 7 and month <= 12 else year  

first_season_id = 1
last_season_id = last_season_yr - first_season_yr

results_url = "https://hnl.hr/povijest/rezultati-i-poretci/?sid={}"
current_results_url = "https://hnl.hr/supersport-hnl/raspored-i-rezultati/"

total_games = 0
total_win = 0
total_lost = 0 
total_draw = 0

def get_tab_content(data):
    content = data.text
    soup = BeautifulSoup(content, 'html.parser')
    tab_content = soup.find(id="tabContent1").div.table
    return tab_content

def prase(tab_content):
    global total_games
    global total_win
    global total_lost
    global total_draw
    for row in tab_content:
        if "class" not in row.attrs:
            cnt = 0

            date = ""
            host = ""
            host_res = ""
            enemy = ""
            enemy_res = "" 

            for child in row.children:
                if cnt == 0:
                    date = child.text[0:17]
                elif cnt == 1:
                    host = child.text
                elif cnt == 2:
                    host_res = child.text
                elif cnt == 4:
                    enemy_res = child.text
                elif cnt == 5:
                    enemy = child.text

                cnt = cnt + 1


            if "Hajduk" in host and "Istra" in enemy and host_res.isnumeric() and enemy_res.isnumeric():

                total_games = total_games + 1

                if int(host_res) > int(enemy_res):
                    print("WON {} vs. {} -> {} - {}, on date {}".format(host, enemy, host_res, enemy_res, date))
                    total_win = total_win + 1
                elif int(host_res) < int(enemy_res):
                    total_lost = total_lost + 1
                    print("LOST {} vs. {} -> {} - {}, on date {}".format(host, enemy, host_res, enemy_res, date))
                else:
                    total_draw = total_draw + 1
                    print("DRAW {} vs. {} -> {} - {}, on date {}".format(host, enemy, host_res, enemy_res, date))

for sid in range(first_season_id, last_season_id):
    data = r.get(results_url.format(sid))
    tab_content = get_tab_content(data)
    if tab_content:
        prase(tab_content)


data_curr = r.get(current_results_url)
tab_content_curr = get_tab_content(data_curr)
if tab_content_curr:
    prase(tab_content_curr)

print("Hajduk WON {}, LOST {}, DRAW {} against Istra on Poljud. TOTAL GAMES {}".format(total_win, total_lost, total_draw, total_games))
    
