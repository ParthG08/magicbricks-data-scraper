import requests
from bs4 import BeautifulSoup
import pandas as pd

city_name = input("Enter a name of your city with first letter being small: ")

url = "https://www.magicbricks.com/ready-to-move-flats-in-" + city_name + "-pppfs"

def saveURL(url,path):
    r = requests.get(url)
    with open(path,"w",encoding="utf-8") as f:
        f.write(r.text)

saveURL(url,"times.html")

with open("times.html","r",encoding="utf8") as file:
    html_doc = file.read()
    
soup = BeautifulSoup(html_doc,"html.parser")
tags = soup.find_all("div", class_="mb-srp__list")

data = {
    'Owner' : [],
    'Carpet Area': [],
    'Status': [],
    'Floor': [],
    'Transaction': [],
    'Furnishing': [],
    'facing':[],
    'overlooking': [],
    'Ownership': [],
    'Bathroom': [],
    'Balcony': [],
    'Price': []
}

for tag in tags:
    labels = tag.find_all("div",class_="mb-srp__card__summary--label")
    label_text = []
    
    for label in labels:
        label_text.append(label.text)
        
    values = tag.find_all("div",class_="mb-srp__card__summary--value")

    n = len(labels)
    for key in data:
        if key in label_text:
            idx = label_text.index(key)
            data[key].append(values[idx].text)
        else:
            data[key].append("--")
    
    data['Price'].pop()
    data['Owner'].pop()
           
    price_div = tag.find("div",class_="mb-srp__card__price--size")
    if price_div:
        price_text = price_div.get_text(strip=True)
        numeric_part = ''.join(filter(str.isdigit, price_text))
        data['Price'].append(numeric_part)
    else:
        data['Price'].append("---")
    
    owner = tag.find("div",class_="mb-srp__card__ads--name")
    data['Owner'].append(owner.text)
    


for key in data:
    # print(key, len(data[key]))
    print(key, data[key])

df = pd.DataFrame(data)
print(df)
file_name = 'Apartments_' + city_name + '.xlsx'
 
df.to_excel(file_name)