import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from commerce.items import AliexpressItem


class ozonSpider(CrawlSpider):
	name = "ozon"
	allowed_domains = ["ozon.ru"]
	start_urls = [
		"http://www.ozon.ru/catalog/1139703/"]

	rules = [
	   # Extract links matching 'item.php' and parse them with the spider's method parse_item
	   Rule(SgmlLinkExtractor(allow='http://www.ozon.ru/context/detail/id/'),follow=True, callback='parse_item')]


	def parse_item(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('.//*[@id="PageContent"]/div[1]/div/div[1]/div[2]/div[1]/h1/text()').extract()
		item['category']= response.xpath('.//*[@id="PageModule"]/div[3]/div[1]/div[4]/div/a/text()').extract()
		item['seller']=response.xpath('..//*[@id="base"]/div[1]/div/div[3]/div/div[2]/div[2]/a/text()').extract()
		#item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		item['itemSpecifics']=response.xpath('.//*[@id="product-desc"]/div[1]/div/dl').extract()
		item['url']=response.xpath('/html/head/meta[7]').extract()
		return item
