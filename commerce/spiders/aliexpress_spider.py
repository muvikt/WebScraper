import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from tutorial.items import AliexpressItem


class aliexpressSpider(CrawlSpider):
	name = "aliexpress"
	allowed_domains = ["aliexpress.com"]
	start_urls = [
		"http://ru.aliexpress.com/premium/category/202005328.html?site=rus&shipCountry=fr&g=y&isrefine=y"]

	rules = [
	   # Extract links matching 'item.php' and parse them with the spider's method parse_item
	   Rule(SgmlLinkExtractor(allow='http://ru.aliexpress.com/item/'), callback='parse_item')]


	def parse_item(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('//div[@class="main-wrap util-clearfix"]//h1/text()').extract()
		item['category']= response.xpath('//html/body/div[3]/div[1]/div/a/text()').extract()
		item['seller']=response.xpath('..//*[@id="base"]/div[1]/div/div[3]/div/div[2]/div[2]/a/text()').extract()
		#item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		item['itemSpecifics']=response.xpath('.//*[@id="product-desc"]/div[1]/div/dl').extract()
		item['url']=response.xpath('/html/head/meta[7]').extract()
		return item

