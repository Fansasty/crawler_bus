from urllib import request
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
count = 0
connect = sqlite3.connect("crawler.db")
db = connect.cursor()
# create tables
db.execute('''CREATE TABLE IF NOT EXISTS route_list
(route TEXT NOT NULL , 
description TEXT NOT NULL)''')
data_request = requests.Session()
connect.commit()
command ={
    "city1":"",
    "city2":"",
    "area":"台北",
    "origin":"臺北轉運站",
    "destination":"朝馬轉運站",
    "area3":"",
    "point":"",
    "search_key":"",
    "submit":"查詢",
    "opt":"search"
}
website_data = data_request.post("http://www.kingbus.com.tw/ticketRoute.php",command) 
soup_data = BeautifulSoup(website_data.text,"html.parser")
select_data = soup_data.select("ul.routeData a") 
with open('crawler.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['route', 'description'])
    for selection_data in select_data:
        data=list()
        temp=selection_data.text.split()
        route = temp[1]
        description = "".join(temp[2:])
        data.append(route)
        data.append(description)
        writer.writerow(data)
        db.execute('''INSERT INTO route_list (route,description) VALUES ('{}','{}')'''.format(route,description))
        connect.commit()
db.execute('''SELECT route FROM route_list''')
rows = db.fetchall()
for row in rows:
    if "埔里" in row[0]:
        count+=1
print("埔里出現"+str(count)+"次")
connect.close

    

 
