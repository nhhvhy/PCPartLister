import discord
import requests
from bs4 import BeautifulSoup

# See the README for info on obtaining a dev token
TOKEN = 'YOUR_TOKEN_HERE'

# Chrome headers worked the best for me, but YMMV
headers = {'user-agent':'Chrome/123.0.0.0'}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_parts(url, headers):
    parts = []
    html = requests.get(url, headers=headers).content
    soup = (BeautifulSoup(html, 'html.parser')).find_all(attrs={'class':'tr__product'})
    soup2 = []

    for element in soup:
        soup2.append(list(element.find_all('a')))

    for i in range(len(soup2)):
        type, name, price, link = 'Other', 'No Part Name', 'No Price Available', 'No Link Available'

        if soup2[i][0]:
            type = soup2[i][0].text.strip()

        if soup2[i][2]:
            name = soup2[i][2].text

        for tag in soup2[i]:
            if 'pp_async_mr' in str(tag.get('class')):
                price = tag.text
                link = tag['href']
                break

        parts.append({'type':type, 'name':name, 'price':price, 'link':link})
    return parts


# Print login username to console
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages sent by the bot to avoid infinite message loops
    if message.author == client.user:
        return
    msg = message.content

    if msg.find("pcpartpicker.com/list/") != -1:
        link_index = msg.index('pcpartpicker.com/list/')
        url = 'https://' + msg[link_index : link_index + 28]
        parts = get_parts(url, headers)

        for part in parts:
            await message.channel.send(part['type'] + ' | ' + part['name'] + ' | ' + part['price'] + '\n')
            # await message.channel.send('_ _')


client.run(TOKEN)