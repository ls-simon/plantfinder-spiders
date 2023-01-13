# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class PlantscraperPipeline:
    def process_item(self, item, spider):  # default method
        # calling dumps to create json data.
        line = json.dumps(dict(item)) + "\n"
        # converting item to dict above, since dumps only intakes dict.
        self.file.write(line)                    # writing content in output file.
        return item
 
    def open_spider(self, spider):
        self.file = open('plants.json', 'w')
 
    def close_spider(self, spider):
        self.file.close()

class MushroomscraperPipeline:
    def process_item(self, item, spider):  # default method
        # calling dumps to create json data.
        line = json.dumps(dict(item)) + "\n"
        # converting item to dict above, since dumps only intakes dict.
        self.file.write(line)                    # writing content in output file.
        return item
 
    def open_spider(self, spider):
        self.file = open('mushrooms.json', 'w')
 
    def close_spider(self, spider):
        self.file.close()

