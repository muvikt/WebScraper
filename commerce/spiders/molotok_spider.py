import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from commerce.items import AliexpressItem
import urlparse 
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class ozonSpider(CrawlSpider):
	name = "molotok"
	allowed_domains = ["molotok.ru"]
	start_urls = [
		"http://www.ozon.ru/catalog/1133731/"]

	rules = [
	   # Extract links matching 'item.php' and parse them with the spider's method parse_item
	   Rule(SgmlLinkExtractor(allow='http://www.ozon.ru/context/detail/id/'),follow=True, callback='parse_item')]


	def parse_item(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('.//*[@class="bItemName"]/text()').extract() 
		item['category']= response.xpath('.//*[@class="bBreadCrumbs jsBreadCrumbs"]/a/text()').extract()
		#item['seller']=response.xpath('..//*[@id="base"]/div[1]/div/div[3]/div/div[2]/div[2]/a/text()').extract()
		item['description'] = response.xpath('.//*[@class="eProductDescriptionText_text"]/p/text()').extract() 
		item['itemSpecifics']=response.xpath('.//*[@class="bItemProperties"]/div/div').extract()
		item['url']=response.xpath('.//*[@rel="canonical"]/@href').extract()
		return item
