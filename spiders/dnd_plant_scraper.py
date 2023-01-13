import scrapy
import re
import random
import json
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from ..items import PlantItem   


CLEANR = re.compile('<.*?>')
data = []


def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def split_at_capitals(raw_html):
    splittet_str = re.findall('([A-Z][^A-Z]*)', raw_html)
    return splittet_str

def get_plant_urls():
    data_into_list = []
    my_file = open("pre_data/links.txt", "r")
    data = my_file.read()
    data_into_list = data.split(",")
    my_file.close()
    return data_into_list



class DndPlantScraperSpider(scrapy.Spider):
    name = 'plants'
    

    def start_requests(self):
        urls = ['https://naturporten.dk/temaer/danmarks-planter/tr%C3%A6er']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        plant_urls = get_plant_urls()
        for plant_url in plant_urls:
            base_url = 'https://www.naturporten.dk'
            yield scrapy.Request(url= base_url + plant_url.strip(), callback=self.parse_element)
      

    def parse_element(self, response):
        base_url = 'https://www.naturporten.dk'
        id = re.findall('(?<=item/).*$', response.url)[0]
        name = response.xpath('//*[@id="yoo-zoo"]/div/div[@class="leksikon_header"]/h1/text()').extract()[0].strip()
        description_block = response.xpath('//*[@class="leksikon_venstre"]//div//p').extract()
        fun_fact = response.xpath('//*[@id="yoo-zoo"]/div/div[3]//div[contains(@class,"box-hint")]//div//text()').extract()[0]
        plant_facts = response.xpath('//*[@id="yoo-zoo"]/div/div[3]//div[contains(@class,"box-info")]//ul//li//text()').extract()
        img_source = ""

        try:
            img_source = response.xpath('//*[@id="yoo-zoo"]/div/div[4]/a/img//@src').extract()[0]
        except:
            img_source = "NO_IMAGE"

        bloom_period = ""
        place_of_growth = plant_facts[1].lower()

        if "skov" in place_of_growth:
            place_of_growth = "woods"
        if "vandløb" in place_of_growth or "kyst" in place_of_growth:
            place_of_growth = "waters"
        if "land" in place_of_growth:
            place_of_growth =  "other"
        

        


        for plant_fact in plant_facts:
            if "blomstrer" in plant_fact.lower():
                try:
                    bloom_period = re.findall('([a-z]+-[a-z]+)', plant_fact.lower())[0]
                except:
                    bloom_period = "UNKNOWN"
        
        item_description_fields = []
        item = {
            'id': id,
            'name_da': name,
            'place_of_growth': place_of_growth,
            'description': {
            'info': fun_fact, 
            'blooming_period': bloom_period,
            },
            'image': img_source,
            'edible': random.choice([True, False])
            } 
        items = PlantItem()

        for field in description_block:
            cleaned_from_tags = cleanhtml(field)
            splited_into_fields = split_at_capitals(cleaned_from_tags)
            item_description_fields.append(splitted_into_fields) 

        for i in range(0,len(item_description_fields[0])):
            
            if "Latinsk" in item_description_fields[0][i]:
                if ":" not in item_description_fields[0][i+1]:
                    item['name_la'] = item_description_fields[0][i+1].strip()
                else:
                    item['name_la'] = "Ikke specificeret"
            if 'Gruppe' in item_description_fields[0][i]:
                if ":" not in item_description_fields[0][i+1]:
                    item['description']['group'] = item_description_fields[0][i+1].strip()
                else:
                    item['description']['group'] = "Ikke specificeret"
                
            if "Klasse" in item_description_fields[0][i]:
                
                if ":" not in item_description_fields[0][i+1]:
                   item['description']['class'] = item_description_fields[0][i+1].strip()
                else:
                    item['description']['class'] = "Ikke specificeret"
            if "Orden" in item_description_fields[0][i]:
                
                if ":" not in item_description_fields[0][i+1]:
                   item['description']['order'] = item_description_fields[0][i+1].strip()
                else:
                    item['description']['order'] = "Ikke specificeret"
            if "Familie" in item:
                item['Beskrivelse'] = ''.join(item_description_fields[2][0:]).strip()
            if "Familie" in item_description_fields[0][i]:
                if ":" not in item_description_fields[0][i+1]:
                    item['description']['family'] = item_description_fields[0][i+1].strip()
                else:
                    item['description']['family'] = "Ikke specificeret"
        
        
       

        items['Plant'] = item
        yield items
        

   
        


    
    