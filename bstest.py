import requests
from bs4 import BeautifulSoup
file = open("testfile.md", "w")

url = "https://pcpartpicker.com/list/dFQv68"
headers = {'user-agent':'Chrome/123.0.0.0'}

def part_finder(url, headers):

    parts = []
    html = requests.get(url, headers=headers).content
    soup = (BeautifulSoup(html, 'html.parser')).find_all(attrs={'class':'tr__product'})
    soup2 = []

    for element in soup:
        soup2.append(list(element.find_all('a')))

    for i in range(len(soup2)):
        type, name, price, link = None
        if soup2[i][0]:
            type = soup2[i][0].text.strip()

        if soup2[i][2]:
            name = soup2[i][2].text

        for tag in soup2[i]:
            if 'pp_async_mr' in str(tag.get('class')):
                price = tag.text
                link = tag['href']
                break

        parts.append([type, name, price, link])
    
    return parts

# find first tag with 'pp_async_mr' class in each product, use for price & href
# for all occurences of <tr> tags, add any with "tr__product" class to a list