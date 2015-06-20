import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from Sevana.items import BplItem
from scrapy.http import FormRequest, Request

class BplSpider(CrawlSpider):
    name = 'bpl'
    start_urls = ['http://103.251.43.95/crdbpl/pubbpllist/xmlpubrankward.php?task=getbplreport&district_code=1603&block_code=1603003&panchayat_code=1603003003&village_code=1603003003004']
    def __init__(self, param="", *args, **kwargs):
        super(BplSpider, self).__init__(*args, **kwargs)
        self.param = param

    def parse(self, response):
        rows = response.xpath("//table[@id='a']/tr")
        for row in rows:
            bpl = BplItem()
            bpl['i1'] = row.xpath("td[2]/text()").extract()
            bpl['i2'] = row.xpath("td[3]/text()").extract()
            bpl['i3'] = row.xpath("td[4]/text()").extract()
            bpl['i4'] = row.xpath("td[5]/text()").extract()
            bpl['i5'] = row.xpath("td[6]/font/text()").extract()
            bpl['i6'] = row.xpath("td[7]/text()").extract()
            bpl['i7'] = row.xpath("td[8]/font/text()").extract()
            bpl['i8'] = row.xpath("td[9]/text()").extract()
            yield bpl
        








