import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from commerce.items import AliexpressItem
import urlparse 
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy import Request



class aliexpressSpider(CrawlSpider):
	name = "aliexpress"
	allowed_domains = ["aliexpress.com"]
	start_urls = ['http://ru.aliexpress.com/all-wholesale-products.html']
		
	#rules = [
	   ## Extract links matching 'item.php' and parse them with the spider's method parse_item
	   #Rule(SgmlLinkExtractor(allow='http://ru.aliexpress.com/item/'),follow=True, callback='parse_item')]
	
	def parse(self, response):
	    '''Parse main page and extract categories links.'''
	    hxs = HtmlXPathSelector(response)
	    urls = hxs.select("//*[@class='sec-categories clearfix']/ul/li/a/@href").extract()
	    for url in urls:
		url = urlparse.urljoin(response.url, url)
		self.log('Found category url: %s' % url)
		yield Request(url, callback = self.parseCategory)

	def parseCategory(self, response):
	    '''Parse category page and extract links of the items.'''
	    hxs = HtmlXPathSelector(response)
	    links = hxs.select("//*[@id='pagination-bottom']/div/a/@href").extract()
	    for link in links:
		itemLink = urlparse.urljoin(response.url, link)
		#self.log('Found item link: %s' % itemLink, log.DEBUG)
		yield Request(itemLink, callback = self.parseComponent)

	def parseComponent(self,response):
	    hxs = HtmlXPathSelector(response)
	    links = hxs.select("//*[@class='detail']/h3/a/@href").extract()
	    for link in links:
		itemLink = urlparse.urljoin(response.url, link)
		#self.log('Found item link: %s' % itemLink, log.DEBUG)
		yield Request(itemLink, callback = self.parseItem)
		
	def parseItem(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('//div[@class="main-wrap util-clearfix"]//h1/text()').extract()
	
		item['category'] = response.xpath("//*[@class='ui-breadcrumb']/a/text()").extract() 
		item['seller']=response.xpath("//*[@class='seller']/div/a/text()").extract()
		#item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		item['itemSpecifics']=response.xpath('.//*[@id="product-desc"]/div[1]/div/dl').extract()
		item['url']=response.xpath('/html/head/meta[7]/@content').extract()
		return item
	      
	      
	#if response.xpath('//html/body/div[3]/div[1]/div/a/text()').extract==[]:
		  #item['category']= response.xpath('//html/body/div[4]/div[1]/div/a/text()').extract
		#else: