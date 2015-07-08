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
	#start_urls = [
		#"http://molotok.ru/otdel/elektronika-tehnika",
		#"http://molotok.ru/otdel/telefony-aksessuary",
		#"http://molotok.ru/otdel/iskusstvo-antikvariat",
		#"http://molotok.ru/otdel/kollekcionirovanie",
		#"http://molotok.ru/otdel/moda-krasota",
		#"http://molotok.ru/otdel/muzyka-knigi-filmy",
		#"http://molotok.ru/otdel/dom-sport",
		#"http://molotok.ru/otdel/avto-zapchasti",
		#"http://molotok.ru/otdel/vse-ostalnoe"]
	start_urls = ["http://molotok.ru/"]

	def parse(self, response):
	    '''Parse main page and extract categories links.'''
	    hxs = HtmlXPathSelector(response)
	    urls = hxs.select('.//*[@class="main-nav clearfix"]/ul/li/div/a/@href').extract()
	    for url in urls:
		url = urlparse.urljoin(response.url, url)
		self.log('Found category url: %s' % url)
		yield Request(url, callback = self.parseCategory)

	def parseCategory(self, response):
	    '''Parse category page and extract links of the items.'''
	    hxs = HtmlXPathSelector(response)
	    links = hxs.select('.//*[@class="category-map-list-wrapper"]/div/ul/li[@class="main-category"]/a/@href').extract()
	    for link in links:
		link="http://molotok.ru"+link
		itemLink = urlparse.urljoin(response.url, link)
		#self.log('Found item link: %s' % itemLink, log.DEBUG)
		yield Request(itemLink, callback = self.parsePages)
		
	def parsePages(self,response):
	    hxs = HtmlXPathSelector(response)
	    numberPages=int(hxs.select('.//*[@id="pager-top"]/ul/li[4]/a/span/text()').extract()[0])
	    numberPagesMax=20 #the maximal number of pages to scrape for each category.
	    currentLink='http://molotok.ru'+str(hxs.select('.//*[@class="next"]/a[1]/@href').extract()[0].split('?')[0])
	    for i in range(2,numberPagesMax):
	      link = currentLink+'?p=%i' %i
	      yield Request(link, callback = self.parseComponent)
		
	def parseComponent(self,response):
	    hxs = HtmlXPathSelector(response)
	    links = hxs.select('.//*[@class="details"]/header/h2/a/@href').extract()
	    for link in links:
		link="http://molotok.ru"+link
		itemLink = urlparse.urljoin(response.url, link)
		#self.log('Found item link: %s' % itemLink, log.DEBUG)
		yield Request(itemLink, callback = self.parse_item)


	def parse_item(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('.//*[@class="main-title"]/h1/text()').extract() 
		item['category']= response.xpath('.//*[@id="breadcrumbs-list"]/li/a/span/text()').extract()
		#item['seller']=response.xpath('..//*[@id="base"]/div[1]/div/div[3]/div/div[2]/div[2]/a/text()').extract()
		item['description'] = response.xpath('.//*[@class="eProductDescriptionText_text"]/p/text()').extract() 
		item['itemSpecifics']=response.xpath('.//*[@class="bItemProperties"]/div/div').extract()
		item['url']=response.xpath('.//*[@rel="canonical"]/@href').extract()
		return item
