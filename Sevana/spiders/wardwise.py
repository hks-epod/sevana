import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from Sevana.items import WardpensionerItem
from Sevana.items import WardItem
from scrapy.http import FormRequest, Request

class WardwiseSpider(CrawlSpider):
    name = 'wardwise'
    f = open("sevana/urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    ward_name = '';

    # start_urls = ['http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=172']
    def __init__(self, param="", *args, **kwargs):
        super(WardwiseSpider, self).__init__(*args, **kwargs)
        self.param = param

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ASP.NET_SessionId':'15w3cy553u25azzc3v4d5t55'}, callback=self.parse)

    def parse(self, response):

        EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]
        VIEWSTATE = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()[0]  

        yield FormRequest.from_response(
            response,
            formname='aspnetForm',
            formdata={  
                '__EVENTTARGET':'ctl00$ContentPlaceHolder1$TabContainerLB$D$lnkviewward',        
                'ctl00_ContentPlaceHolder1_TabContainerLB_ClientState': '{"ActiveTabIndex":0,"TabState":[true,true,true,true]}',
                'ctl00$ContentPlaceHolder1$TabContainerLB$B$ddCategory':'0',
                'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender':'0',
                '__LASTFOCUS:': '',
                '__EVENTARGUMENT':'',
                '__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR':'EDCABF3B',
                '__EVENTVALIDATION':EVENTVALIDATION
            },
            callback=self.wardResults
        )

    def wardResults(self, response):
        rows = response.xpath("//table[@id='ctl00_ContentPlaceHolder1_TabContainerLB_D_dgvWard_DXMainTable']/tbody/tr")
        for row in rows:
            global ward_name
            ward_name = row.xpath("td[2]/font/text()").extract()

            # ward = WardItem()
            # ward['ward_id']= row.xpath("td[1]/font/text()").extract()
            # ward['ward_name'] = row.xpath("td[2]/font/text()").extract()
            # ward['ALP'] = row.xpath("td[3]/font/a/text()").extract()
            # ward['NOAP']= row.xpath("td[4]/font/a/text()").extract()
            # ward['MCP']= row.xpath("td[5]/font/a/text()").extract()
            # ward['PHP']= row.xpath("td[6]/font/a/text()").extract()
            # ward['UMWP']= row.xpath("td[7]/font/a/text()").extract()
            # ward['WP']=row.xpath("td[8]/font/a/text()").extract()
            # yield ward

            ward_detail = row.xpath("td[9]/font/a/@href").extract()[0]
            link = 'http://www.welfarepension.lsgkerala.gov.in/' + ward_detail
            yield Request(link, self.getwardDetails)

    def getwardDetails(self, response):

        rows = response.xpath("//*[@id='ctl00_ContentPlaceHolder1_Grd1_DXMainTable']/tbody/tr")
        for row in rows:
            global ward_name
            pensioner = WardpensionerItem()
            pensioner['ward_name'] = ward_name
            pensioner['pensioner_id'] = row.xpath("td[1]/font/text()").extract()
            pensioner['pensioner_name'] = row.xpath("td[2]/font/text()").extract()
            pensioner['ward_last_disbursed_month'] = row.xpath("td[4]/font/text()").extract()
            yield pensioner




