import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from Sevana.items import SevanaItem
from scrapy.http import FormRequest, Request

class PensionSpider(CrawlSpider):
    name = 'pension'
    start_urls = [
        'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=172',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=189',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=171',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=209',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=210',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=215',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=218',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=167',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=760',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=407',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=514',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=610',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=350',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=734',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=225',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=391',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=366',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=723',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=1223',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=776',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=811',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=248',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=918',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=277',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=697',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=843',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=1052',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=313',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=1091',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=912',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=504',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=1130',
        # 'http://www.welfarepension.lsgkerala.gov.in/LBWiseEng.aspx?lbid=524',
    ]

    def __init__(self, isHistory="", *args, **kwargs):
        super(PensionSpider, self).__init__(*args, **kwargs)
        self.isHistory = isHistory

        self.PensionType = {
            '1' : 'Agricultural Labour Pension',
            '2' :'Indira Gandhi National Old Age Pension',
            '3' :'Pension for the Mentally challenged',
            '4' :'Pension for the Physically challenged',
            '5' :'Pension for the  Unmarried Women above 50 years',
            '6' :'Widow Pension'
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ASP.NET_SessionId':'hwhyrd45h0czhbvq41whas55'}, callback=self.parse)

    def parse(self, response):

        # Change pension type and feth results
        for x in range(1, 7):
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
                }, 
                callback=self.pensionResults
            )

    def pensionResults(self, response):
        print response.body

        Pensioner ID = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()[0]


//*[@id="ctl00_ContentPlaceHolder1_TabContainerLB_A_dgvLBPentype"]/tbody/tr[2]
        



        # item = SevanaItem()

        #  Fetch data here
        # item['NitricOxide'] = response.xpath("//*[@id='Head1']/title/text()").extract()[0]
        # yield item








