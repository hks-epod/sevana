import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from Sevana.items import PensionerItem
from scrapy.http import FormRequest, Request

class PensionSpider(CrawlSpider):
    name = 'pension'
    # f = open("sevana/urls.txt")
    # start_urls = [url.strip() for url in f.readlines()]
    # f.close()
    start_urls = ['http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=172']
    def __init__(self, param="", *args, **kwargs):
        super(PensionSpider, self).__init__(*args, **kwargs)
        self.param = param
        self.PensionType = {
            1 : 'Agricultural Labour Pension',
            2 :'Indira Gandhi National Old Age Pension',
            3 :'Pension for the Mentally challenged',
            4 :'Pension for the Physically challenged',
            5 :'Pension for the  Unmarried Women above 50 years',
            6 :'Widow Pension'
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ASP.NET_SessionId':'il2wvg45mphe5i452sl4kjfp'}, callback=self.parse)

    def parse(self, response):

        # Change pension type and feth results
        for x in range(1,2):
            EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]
            VIEWSTATE = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()[0]  

            yield FormRequest.from_response(
                response,
                formname='aspnetForm',
                formdata={  
                    '__EVENTTARGET':'ctl00$ContentPlaceHolder1$TabContainerLB$A$ddPenType',        
                    'ctl00_ContentPlaceHolder1_TabContainerLB_ClientState': '{"ActiveTabIndex":0,"TabState":[true,true,true,true]}',
                    'ctl00$ContentPlaceHolder1$TabContainerLB$A$ddPenType' :str(x),
                    'ctl00$ContentPlaceHolder1$TabContainerLB$B$ddCategory':'0',
                    'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender':'0',
                    '__LASTFOCUS:': '',
                    '__EVENTARGUMENT':'',
                    '__VIEWSTATE': VIEWSTATE,
                    '__EVENTVALIDATION':EVENTVALIDATION
                },cookies={'ASP.NET_SessionId':'il2wvg45mphe5i452sl4kjfp'},
                callback=self.pensionResults
            )

    def pensionResults(self, response):
        rows = response.xpath("//table[@id='ctl00_ContentPlaceHolder1_TabContainerLB_A_dgvLBPentype']/tr")
        for row in rows:
            pensioner = PensionerItem()
            pensioner['pensioner_id'] = row.xpath("td[1]/font/text()").extract()
            pensioner['pensioner_name'] = row.xpath("td[2]/font/text()").extract()
            # pensioner['address'] = row.xpath("td[3]/font/text()").extract()
            pensioner['last_disbursed_month'] = row.xpath("td[4]/font/text()").extract()
            pensioner['pension_type'] = response.xpath("//select[@id='ctl00_ContentPlaceHolder1_TabContainerLB_A_ddPenType']/option[@selected='selected']/text()").extract()
            yield pensioner

        # Follow next page if nest is there
        isNext= response.xpath("//input[@id='ctl00_ContentPlaceHolder1_TabContainerLB_A_imgbtnNext']//@disabled").extract()
        ptype_index= response.xpath("//select[@id='ctl00_ContentPlaceHolder1_TabContainerLB_A_ddPenType']/option[@selected='selected']//@value").extract()
        EV = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]
        VS = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()[0]  
        if isNext == []:
            yield FormRequest.from_response(
                 response,
                 formname='aspnetForm',
                 formdata={  
                     '__EVENTTARGET':'ctl00$ContentPlaceHolder1$TabContainerLB$A$ddPenType',        
                     'ctl00_ContentPlaceHolder1_TabContainerLB_ClientState': '{"ActiveTabIndex":0,"TabState":[true,true,true,true]}',
                     'ctl00$ContentPlaceHolder1$TabContainerLB$A$ddPenType' :str(ptype_index),
                     'ctl00$ContentPlaceHolder1$TabContainerLB$B$ddCategory':'0',
                     'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender':'0',
                     '__LASTFOCUS:': '',
                     '__EVENTARGUMENT':'',
                     '__VIEWSTATE': VS,
                     '__EVENTVALIDATION':EV,
                     'ctl00$ContentPlaceHolder1$TabContainerLB$A$imgbtnNext.x':'8',
                    'ctl00$ContentPlaceHolder1$TabContainerLB$A$imgbtnNext.y':'7'
                 },cookies={'ASP.NET_SessionId':'il2wvg45mphe5i452sl4kjfp'},
                 callback= self.pensionResults
            )








