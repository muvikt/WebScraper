# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'commerce'

SPIDER_MODULES = ['commerce.spiders']
NEWSPIDER_MODULE = 'commerce.spiders'
DOWNLOAD_DELAY= .5
ITEM_PIPELINES = {'commerce.pipelines.JsonWithEncodingPipeline'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'commerce (+http://www.yourdomain.com)'
