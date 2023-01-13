# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlantItem(scrapy.Item):

    Plant = scrapy.Field()


class MushroomItem(scrapy.Item):

    Mushroom = scrapy.Field()
