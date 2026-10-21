import scrapy
from crawldata.items import CrawldataItem

class MohoSpider(scrapy.Spider):
    name = "homeoffice"
    allowed_domains = ["homeoffice.com.vn"]
    start_urls = [
      f"https://homeoffice.com.vn/noi-that-van-phong-page-{i}.html?items_per_page=16"
      for i in range(1, 25)
  ]

    def parse(self, response):
        productURLs = response.xpath('//div[@class="ty-grid-list__item-name"]/descendant::a/@href').getall()
        for productURL in productURLs:
            product = CrawldataItem()
            product["ProductURL"] = response.urljoin(productURL)
            request = scrapy.Request(url = response.urljoin(productURL) , callback=self.parseProduct)
            request.meta['product'] = product
            yield request
    def parseProduct(self, response):
        product = response.meta['product']
        product['ProductID'] =  response.xpath('//span[@class="ty-control-group__item"]/text()').get().strip()
        product['ProductName'] =  response.xpath('//h1[@class="ty-product-block-title"]/text()').get().strip()
        product["Category"] = response.xpath('//a[@class="ty-breadcrumbs__a"]/text()').getall()[-1].strip()
        product["Price"] = response.xpath('//span[@class="ty-price-num"]/text()').get().strip()
        product["Material"] = response.xpath('//div[@id="content_description"]//li[contains(., "Chất liệu") or contains(., "chất liệu")]/text()').get().strip()
        product["Dimensions"] = response.xpath('//div[@id="content_description"]//li[contains(., "Kích thước") or contains(., "kích thước")]/text()').get().strip()
        yield product