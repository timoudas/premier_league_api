from bs4 import BeautifulSoup as soup
import requests
from lxml import html
from pprint import pprint
player_page = requests.get('https://www.premierleague.com/clubs/43/Burnley/squad')
cont = soup(player_page.content, 'lxml')
key_number = [key for element in cont.select('span.number') for key in element['class']]
key_name = [key for element in cont.select('h4.name') for key in element['class']]
key_position = [key for element in cont.select('span.position') for key in element['class']]

data = {
        inner_k: v.get_text(strip=True)
        for k,v in zip((number,name,position), cont.select('span.number', 'h4.name', 'span.position')) for (number,name,position) in zip(key_number,key_name,key_position)  
    } 