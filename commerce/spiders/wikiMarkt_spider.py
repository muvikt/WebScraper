import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from commerce.items import AliexpressItem
import urlparse 
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class ozonSpider(CrawlSpider):
	name = "wikimarkt"
	allowed_domains = ["ozon.ru"]
	#handle_httpstatus_list = [302,301]
	#Request.meta = {'dont_redirect': True,
		    #'handle_httpstatus_list': [301]}
	start_urls = [
		"http://www.ozon.ru/context/div_book/?localredirect=no",
		"http://www.ozon.ru/context/div_tech/?localredirect=no",
		"http://www.ozon.ru/context/div_appliance/?localredirect=no",
		"http://www.ozon.ru/context/div_home/?localredirect=no",
		"http://www.ozon.ru/context/div_kid/?localredirect=no",
		"http://www.ozon.ru/context/div_beauty/?localredirect=no",
		"http://www.ozon.ru/context/div_bs/?localredirect=no",
		"http://www.ozon.ru/context/div_fashion/?localredirect=no",
		"http://www.ozon.ru/context/div_soft/?localredirect=no",
		"http://www.ozon.ru/context/div_dvd/?localredirect=no",
		"http://www.ozon.ru/context/div_music/?localredirect=no",
		"http://www.ozon.ru/context/div_rar/?localredirect=no"]
	
	#start_urls = [
		#"http://www.ozon.ru/context/div_book/?localredirect=no"]

	#rules = [
	    ## Extract links matching 'item.php' and parse them with the spider's method parse_item
	    #Rule(SgmlLinkExtractor(allow='http://www.ozon.ru/context/detail/id/'), follow=True, callback='parse_item')]
	
	def parse(self, response):
	    #'''Parse main page and extract categories links.'''
	      #print 'YES'
	      #hxs = HtmlXPathSelector(response)
	      print response
	      urls = response.xpath('.//*[@id="TDpageLeft"]/div[1]/div/div/a[@class="eLeftMainMenu_Link "]/@href').extract()
	      for url in urls:
		  url_orig=url
		  nbMaxPages=15
		  for i in range(0,nbMaxPages):
		    url=url.split("?")[0]
		    url='http://www.ozon.ru'+url_orig+"?localredirect=no&page=%i" %i
		    url = urlparse.urljoin(response.url, url)
		    self.log('Found category url: %s' % url)
		    yield Request(url,callback = self.parse_categorie)
	  
	def parse_categorie(self,response):
	  #rules = [
	    ## Extract links matching 'item.php' and parse them with the spider's method parse_item
	    #Rule(SgmlLinkExtractor(allow='http://www.ozon.ru/context/detail/id/'), follow=True, callback='parse_item')]
	    
	    #hxs = HtmlXPathSelector(response)
	    links =response.xpath("//*[@class='bOneTile inline jsUpdateLink ']/a/@href").extract()
	    for link in links:
		if '#comments_list' in link:
		  links.remove(link)
		else: 
		  link='http://www.ozon.ru'+link
		  itemLink = urlparse.urljoin(response.url, link)
		  #self.log('Found item link: %s' % itemLink, log.DEBUG)
		  yield Request(itemLink, callback = self.parse_item)


	def parse_item(self, response):
	    # Extract necessary information (whith is definite in items.py)
		item = AliexpressItem()
		#item['id'] = response.xpath('//h1[@id="product-name"]/text()').re(r'ID: (\d+)')
		item['title'] = response.xpath('.//h1/text()').extract()
		item['category']= response.xpath('.//*[@class="bBreadCrumbs jsBreadCrumbs"]/a/text()').extract()
		#item['seller']=response.xpath('..//*[@id="base"]/div[1]/div/div[3]/div/div[2]/div[2]/a/text()').extract()
		item['description'] = response.xpath('.//*[@class="eProductDescriptionText_text"]/p/text()').extract() 
		item['itemSpecifics']=response.xpath('.//*[@class="bItemProperties"]/div/div').extract()
		item['url']=response.xpath('.//*[@rel="canonical"]/@href').extract()
		return item
