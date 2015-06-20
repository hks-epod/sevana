import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from Sevana.items import PensionerItem
from scrapy.http import FormRequest, Request

class GenderSpider(CrawlSpider):
    name = 'genderwise'
    # f = open("sevana/urls.txt")
    # start_urls = [url.strip() for url in f.readlines()]
    # f.close()
    start_urls = ['http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=172']
    def __init__(self, param="", *args, **kwargs):
        super(GenderSpider, self).__init__(*args, **kwargs)
        self.param = param
        self.page= 1
        self.gender = {
            1 : 'Male',
            2 :'Female',
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ASP.NET_SessionId':'il2wvg45mphe5i452sl4kjfp'}, callback=self.parse)

    def parse(self, response):
        # Change pension type and feth results
        for x in range(1,3):
            EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]
            VIEWSTATE = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()[0]  

            yield FormRequest.from_response(
                response,
                formname='aspnetForm',
                formdata={  
                    '__EVENTTARGET':'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender',        
                    'ctl00_ContentPlaceHolder1_TabContainerLB_ClientState': '{"ActiveTabIndex":0,"TabState":[true,true,true,true]}',
                    'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender':str(x),
                    '__LASTFOCUS:': '',
                    '__EVENTARGUMENT':'',
                    '__VIEWSTATE': VIEWSTATE,
                    '__EVENTVALIDATION':EVENTVALIDATION
                }, 
                callback=self.pensionResults
            )

    def pensionResults(self, response):
        rows = response.xpath("//table[@id='ctl00_ContentPlaceHolder1_TabContainerLB_C_dgvGender']/tr")
        for row in rows:
            pensioner = PensionerItem()
            pensioner['pensioner_id'] = row.xpath("td[1]/font/text()").extract()
            pensioner['pensioner_name'] = row.xpath("td[2]/font/text()").extract()
            # pensioner['address'] = row.xpath("td[3]/font/text()").extract()
            pensioner['last_disbursed_month'] = row.xpath("td[4]/font/text()").extract()
            pensioner['gender'] = response.xpath("//select[@id='ctl00_ContentPlaceHolder1_TabContainerLB_C_ddGender']/option[@selected='selected']/text()").extract()
            yield pensioner

        # Follow next page if nest is there


        isNext= response.xpath("//*[@id='ctl00_ContentPlaceHolder1_TabContainerLB_C_dgvGender']/tbody/tr[32]/td/table/tbody/tr/td[12]/input//@disabled").extract()
        ptype_index= response.xpath("//select[@id='ctl00_ContentPlaceHolder1_TabContainerLB_C_ddGender']/option[@selected='selected']//@value").extract()
        EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]
        VIEWSTATE = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()[0]  

        page = 'Page$'+ str(self.page)
        self.page = self.page+1
        print '***********************************'
        print page

        if isNext == []:
            yield FormRequest.from_response(
                 response,
                 formname='aspnetForm',
                 formdata={  
                     '__EVENTTARGET':'ctl00$ContentPlaceHolder1$TabContainerLB$A$ddPenType',        
                     'ctl00_ContentPlaceHolder1_TabContainerLB_ClientState': '{"ActiveTabIndex":0,"TabState":[true,true,true,true]}',
                     'ctl00$ContentPlaceHolder1$TabContainerLB$C$ddGender':str(ptype_index),
                     '__LASTFOCUS:': '',
                     '__EVENTARGUMENT':page,
                     '__VIEWSTATE': VIEWSTATE,
                     '__EVENTVALIDATION':EVENTVALIDATION
                 }, 
                 callback= self.pensionResults
            )








