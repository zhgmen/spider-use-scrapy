import scrapy

class DygodSpider(scrapy.Spider):
    name = 'dygod'
    allowed_domains = ["dygod.net"]
    def start_requests(self):
        urls = [
            'https://www.dygod.net',
            ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    
    def parse(self, response):
        domain = response.url
        for url in response.css('div.title_all p span a::attr(href)'):
            url_top = domain + url.extract()
            yield scrapy.Request(url=url_top, callback=self.parse_top, meta={
                'domain': domain,

                })

    def parse_top(self, response):
        
        for table in response.css('table.tbspan'):
            
            _, title, times, desc = table.css('tr')
            name =  title.css('a::text').get()
            url = response.meta['domain'] + title.css('a::attr(href)').get()
            time = times.css('td')[1].css('::text').getall()[1]
            description = desc.css('td::text').get()
            #yield dict(title=table.extract())
            yield scrapy.Request(url=url, callback=self.parse_html, meta={
                })

        next_page = response.css('div.title_all p em a::attr(href)')
        length = len(next_page.getall())
        if length != 0:
            for page in next_page:
                url = response.meta['domain'] + page.extract()
                pages = response.urljoin(url)
                yield scrapy.Request(url=pages, callback=self.parse_top)

    def parse_html(self, response):
        downurl = response.css('table')[1].css('::attr(href)').getall()
        
    
