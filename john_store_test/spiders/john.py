import scrapy


class JohnSpider(scrapy.Spider):
    name = "john"
    allowed_domains = ["gopher1.extrkt.com"]
    start_urls = ["https://gopher1.extrkt.com/"]

    def parse(self, response):
        products_urls = response.xpath("//ul[@class='products columns-4']/li/a[@class='woocommerce-LoopProduct-link woocommerce-loop-product__link']/@href")
        for url in products_urls:
            yield scrapy.Request(url=url.get(),callback=self.results_parse)

        next_page_url = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

        


    def results_parse(self, response):
        Category_=response.xpath('//nav[@class="woocommerce-breadcrumb"]/a/text()').getall()
        path='/'.join(Category_) 
        Product_title = response.xpath("//h1//text()").get()
        Price = response.xpath("//p[@class='price']/span/bdi/text()").get()
        Currency_symbol = response.xpath("//p[@class='price']//span[@class='woocommerce-Price-currencySymbol']/text()").get()
        Size = response.xpath("//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_size']/td/p/text()").get()
        Color = response.xpath("//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_color']/td/p/text()").get()
        SKU=response.xpath('//span[@class="sku_wrapper"]/span/text()').get()
        Description=response.xpath('//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab"]/p/text()').getall()
        Category=response.xpath('//span[@class="posted_in"]/a/text()').get()
        thumbnail=response.xpath('//div[@data-thumb]/a/img/@src').get()
        


        
        yield {
            "path":path,
            "product_title":Product_title,
            "price":Currency_symbol + Price, 
            "size":Size,
            "color":Color, 
            "SKU":SKU,
            "Description":Description,
            "Category":Category,
            "thumbnail":thumbnail

        }
