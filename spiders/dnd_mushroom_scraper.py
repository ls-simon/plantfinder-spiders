import json
import urllib
import string
import random
import scrapy
from ..items import MushroomItem   
import re 

is_text_filter = re.compile('([A-Za-z ]{2,})')
base_url = 'http://www.svampeguide.dk/'  

class MushroomScraper(scrapy.Spider):
    name = "mushrooms"
    #allowed_domains = ["http://www.svampeguide.dk"]
    start_urls = [
        "http://www.svampeguide.dk/alle-svampe"
    ]

    def parse(self, response):
        
        uris = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "alfa")]//div//a//@href').extract()
        for uri in uris:
            yield scrapy.Request(base_url + str(uri), callback=self.parse_page)

    def parse_page(self, response):
       
        id = re.findall('(?<=svampeguide.dk/).*$', response.url)[0]
        items = MushroomItem()
        print(response.url)
        name_da = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "header")]//h1//text()').extract()[0]
        name_la = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "header")]//div//text()').extract()[0]
        image_url = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "data")]//div[@id="pic-div"]//img//@src').extract()[0]
        is_edible = ""
        fact_keyvalue_list = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "data")]//div[@class="sections"]//div[@class="prop"]//text()').extract()
        is_text_filtered = [i.strip() for i in fact_keyvalue_list]
        description_key_value = [i for i in is_text_filtered if i]
        
        mushroom = {
            'id': id,
            'name_da': name_da,
            'name_la': name_la,
            'image': base_url + image_url,
            
            'description': {
                'group': 'svampe'
            }
            }

        for i in range(0,len(description_key_value),2):
    
            if "voksemåde" in description_key_value[i].lower():
                mushroom['description']['voksemåde'] = description_key_value[i+1] 
                mushroom['description']['info_text_box'] = ''.join(description_key_value[i+2:])
                break
            mushroom['description'][description_key_value[i].lower()] = description_key_value[i+1]

        place_of_growth = ""
        if "skov" in mushroom['description']['voksested']:
            place_of_growth = "woods"
        else:
            place_of_growth = "other"
        mushroom['place_of_growth'] = place_of_growth
        

        info_text_box = mushroom['description']['info']

        is_edible = False

        try:
            edible_from_image = response.xpath('/html/body/div[@id="wrap"]//div[@id="main"]//div//div[contains(@class, "data")]//div[@class="sections"]//div[@class="prop"]//img//@src').extract()[0]
            if ("edible" in edible_from_image):
                is_edible = True
            elif ("poison" in edible_from_image):
                is_edible = False
            else:
                edible_from_description = get_edible_from_info(info_text_box)
                is_edible = edible_from_description
        except:
            is_edible = get_edible_from_info(info_text_box)

        mushroom['edible'] = is_edible

        items['Mushroom'] = mushroom
        yield items
     
def get_edible_from_info(info_text_box):
    is_edible = True
    for info_str in info_text_box:
        desc = info_str.lower()
        if ("spisesvamp" in desc):
            is_edible = True
        elif ("frarådes" in desc):
            is_edible = False
        elif ("gift" in desc):
            is_edible = False
        elif ("ikke spiselig" in desc):
            is_edible = False
        elif ("spiselig" in desc):
            is_edible = True
        elif ("smag" in desc):
            is_edible = True
        elif ("lægemiddel" or "l\u00e6gemiddel" in desc):
            is_edible = True
        
    return is_edible
        