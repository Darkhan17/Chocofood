import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', #pylint: disable =line-too-long
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', #pylint: disable =line-too-long
    'Application-Model':'ProductListInfo',
    'Content-Type':'application/json',
}




def to_int(price):
    """"Convert string to number"""
    if isinstance(price,int):
        return price
    elif isinstance(price,float):
        return int(price)
    else:
        new_price = re.findall(r'\d+', price)
        number = ""
        for i in new_price:
            number+=i
        return int(number)



class Parsing:
    """Base parcing classs"""
    urls={}
    def get_html(self,url,params=''):
        """Making request to url and get html"""
        html = requests.get(url,params,headers=HEADERS)
        return html

    def parse(self,category):
        """Checking connection """
        url = self.urls[category]
        html = self.get_html(url)
        products = []
        if html.status_code==200:
            html = self.get_html(url,)
            products.extend(self.get_content(html.text,category))
        return products

    def get_content(self,html,category):
        """get data from parsing websites"""


class SulpakParsing(Parsing):
    """Sulpak parcing"""
    HOST = 'https://www.sulpak.kz'
    URL_IPHONE = 'https://www.sulpak.kz/f/smartfoniy/almaty/1056_62'
    URL_TV = 'https://www.sulpak.kz/f/led_oled_televizoriy'
    URL_NOTEBOOK = 'https://www.sulpak.kz/f/noutbuki'
    URL_REFRIGIRATOR = 'https://www.sulpak.kz/f/holodilniki'
    URL_WATCH = 'https://www.sulpak.kz/f/smart_chasiy'
    URL_СLEANER = 'https://www.sulpak.kz/f/piylesosiy'
    URL_TABLETS = 'https: // www.sulpak.kz / f / planshetiy_graficheskie'
    URL_DISHWASHER='https://www.sulpak.kz/f/posudomoechniye_mashiniy'
    URL_FANS = 'https://www.sulpak.kz/f/ventilyatoriy'
    URL_RAZORS ='https://www.sulpak.kz/f/britviy_i_epilyatoriy'

    urls = {'Notebooks':URL_NOTEBOOK, 'Iphones':URL_IPHONE,'TV':URL_TV,'Refrigerators':URL_REFRIGIRATOR,
            'Watches':URL_WATCH,'Cleaners':URL_СLEANER, 'Tablets':URL_TABLETS, 'Dishwashers':URL_DISHWASHER, 'FANS':URL_FANS,
            'Razors':URL_RAZORS} #pylint: disable =line-too-long


    def get_content(self,html,category):
        flag = True
        products = [{'shop':'Sulpak','category':category,'items':list()}]
        while flag:
            soup = BeautifulSoup(html,'lxml')
            next_page = soup.find('a', class_='next')
            if hasattr(next_page, 'href'):
                try:
                    extra_url = next_page.attrs['href']
                    html = self.get_html(self.HOST + extra_url).text
                except (AttributeError, KeyError):
                    flag = False
            else:
                flag = False
            items = soup.find_all('li',class_='tile-container')
            for item in items:
                try:
                    products[0]['items'].append({
                        'title' : item.find('h3', class_= 'title').get_text(strip=True),
                        'price' : item.find('div',class_='price').get_text(strip=True)
                    })
                except (AttributeError,KeyError):
                    break
        return products

class TechnodomParsing():
    """Technodom parsing"""
    URL_IPHONE = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:smartfony-i-gadzhety/smartfony-i-telefony/smartfony},brands:{in:[215616]}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0' #pylint: disable =line-too-long
    URL_TV = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:tv-audio-foto-video/televizory/led-televizory}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0' #pylint: disable =line-too-long
    URL_NOTEBOOK = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0' #pylint: disable =line-too-long
    URL_REFRIGIRATOR = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:bytovaja-tehnika/hranenie-produktov-i-napitkov/holodil-niki}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0' #pylint: disable =line-too-long
    URL_WATCH = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:smartfony-i-gadzhety/gadzhety/smart-chasy}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0'
    URL_СLEANER = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:bytovaja-tehnika/uhod-za-domom/pylesosy}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0'
    URL_TABLETS = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:smartfony-i-gadzhety/planshety-i-jelektronnye-knigi/planshety}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0'
    URL_DISHWASHER = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:bytovaja-tehnika/uhod-za-domom/posudomoechnye-mashiny}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0'
    URL_FANS = 'https://www.technodom.kz/graphql?hash=2765882266&_url_path_0=bytovaja-tehnika/klimaticheskaja-tehnika/ventiljatory'
    URL_RAZOR = 'https://www.technodom.kz/graphql?hash=4008966576&_currentPage_0=1&_pageSize_0=24&_filter_0={category_url_path:{eq:krasota-i-zdorov-e/muzhskoj-uhod/jelektrobritvy}}&_sort_0={score:DESC}&_attributes_0=sticker,brands&_isNightSalesActive_0=0'

    HOST = 'https://www.technodom.kz/'

    urls = {'Notebooks': URL_NOTEBOOK, 'Iphones': URL_IPHONE, 'TV': URL_TV, 'Refrigerators': URL_REFRIGIRATOR,
            'Watches': URL_WATCH, 'Cleaners': URL_СLEANER, 'Tablets': URL_TABLETS, 'Dishwashers': URL_DISHWASHER,
            'FANS': URL_FANS,
            'Razors': URL_RAZOR}  # pylint: disable =line-too-long

    def parse(self,category):
        products = [{'shop': 'Technodom', 'category': category, 'items': list()}]
        current_page=1
        url = self.urls.get(category)
        data  = requests.get(url,headers = HEADERS).json()
        last_page = data['data']['products']['page_info']['total_pages']
        for i in range(current_page,last_page+1):
            data = requests.get(url,headers=HEADERS,params={'_currentPage_0':i}).json()
            items = data['data']['products']['items']
            for item in items:
                products[0]['items'].append({
                    'title': item['name'],
                    'price': item['price']['minimalPrice']['amount']['value']
                })
        return products

class MechtaParsing():
    """Mechta parsing"""
    URL_IPHONE = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&filter=true'
    URL_IPHONE_DATA ='https://www.mechta.kz/api/main/catalog_new/index.php?section=apple-eql&catalog=true&page_element_count=18' #pylint: disable =line-too-long
    URL_TV = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=televizory&filter=true'
    URL_TV_DATA ='https://www.mechta.kz/api/main/catalog_new/index.php?section=televizory&page_num=2&catalog=true&page_element_count=18' #pylint: disable =line-too-long
    URL_REFRIGERATOR = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=holodilniki&filter=true' #pylint: disable =line-too-long
    URL_REFRIGERATOR_DATA ='https://www.mechta.kz/api/main/catalog_new/index.php?section=holodilniki&page_num=2&catalog=true&page_element_count=18' #pylint: disable =line-too-long
    URL_NOTEBOOK = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&filter=true' #pylint: disable =line-too-long
    URL_NOTEBOOK_DATA='https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&page_num=2&catalog=true&page_element_count=' #pylint: disable =line-too-long
    URL_WATCH = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=smart-chasy&filter=true'
    URL_WATCH_DATA ='https://www.mechta.kz/api/main/catalog_new/index.php?section=smart-chasy&page_num=2&catalog=true&page_element_count=18'
    URL_CLEANER = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=pylesosy&filter=true'
    URL_CLEANER_DATA = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=pylesosy&page_num=2&catalog=true&page_element_count=18'
    URL_TABLETS = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=planshety&filter=true'
    URL_TABLETS_DATA = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=planshety&page_num=2&catalog=true&page_element_count=18'
    URL_DISHWASHER = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=posudomoechnye-mashiny&filter=true'
    URL_DISHWASHER_DATA = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=posudomoechnye-mashiny&filter=true'
    URL_FANS = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=ventilyatory&filter=true'
    URL_FANS_DATA ='https://www.mechta.kz/api/main/catalog_new/index.php?section=ventilyatory&filter=true'
    URL_RAZOR = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=elektrobritvy&filter=true'
    URL_RAZOR_DATA = 'https://www.mechta.kz/api/main/catalog_new/index.php?section=elektrobritvy&page_num=2&catalog=true&page_element_count=18'


    urls = {'Notebooks': URL_NOTEBOOK, 'Iphones': URL_IPHONE, 'TV': URL_TV, 'Refrigerators': URL_REFRIGERATOR,
            'Watches': URL_WATCH, 'Cleaners': URL_CLEANER, 'Tablets': URL_TABLETS, 'Dishwashers': URL_DISHWASHER,
            'FANS': URL_FANS,
            'Razors': URL_RAZOR}  # pylint: disable =line-too-long




    def parse(self,category):
        """Parse website"""
        url,url_data = self.urls[category][0],self.urls[category][1]
        html = requests.get(url).json()
        products = [{'shop': 'Mechta', 'category': category, 'items': list()}]

        url_get = url_data + str(html['data']['all'])
        data = requests.get(url_get).json()
        for i in data['data']['ITEMS']:
            try:
                products[0]['items'].append(
                    { 'title' : i['NAME'],
                      'price' : i['PRICE']['PRICE'],
                    })
            except KeyError:
                continue
        return products

class BeliyVeterParsing(Parsing):
    """Beiyveter parcing"""
    URL_IPHONE = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/fltr_brand-is-apple/apply/' #pylint: disable =line-too-long
    URL_TV = 'https://shop.kz/televizory/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_NOTEBOOK = 'https://shop.kz/noutbuki/filter/clear/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/' #pylint: disable =line-too-long
    URL_REFRIGIRATOR = 'https://shop.kz/kholodilniki/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/' #pylint: disable =line-too-long
    URL_WATCH = 'https://shop.kz/smart-chasy/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_CLEANER = 'https://shop.kz/pylesosy/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_TABLETS = 'https://shop.kz/planshety/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_DISHWASHER = 'https://shop.kz/posudomoechnye-mashiny/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_FANS = 'https://shop.kz/ventilyatory/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    URL_RAZOR = 'https://shop.kz/elektrobritvy-epilyatory/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'

    HOST = 'https://shop.kz'


    urls = {'Notebooks': URL_NOTEBOOK, 'Iphones': URL_IPHONE, 'TV': URL_TV, 'Refrigerators': URL_REFRIGIRATOR,
            'Watches': URL_WATCH, 'Cleaners': URL_CLEANER, 'Tablets': URL_TABLETS, 'Dishwashers': URL_DISHWASHER,
            'FANS': URL_FANS,
            'Razors': URL_RAZOR}  # pylint: disable =line-too-long

    def get_content(self,html,category):
        flag = True
        products = [{'shop':'Beliyveter','category':category,'items':list()}]
        while flag:
            soup = BeautifulSoup(html, 'lxml')
            next_page = soup.find('li', class_='bx-pag-next').find('a')
            if hasattr(next_page, 'href'):
                try:
                    extra_url = next_page.attrs['href']
                    html = self.get_html(self.HOST + extra_url).text
                except AttributeError:
                    flag = False
            else:
                flag = False
            items = soup.find_all('div', class_='bx_catalog_item double') #pylint: disable =line-too-long
            for item in items:
                products[0]['items'].append({
                    'title': item.find('div',class_ = 'bx_catalog_item_title').a.get_text(strip=True),
                    'price': item.find('span', class_= 'bx-more-price-text').get_text(strip=True),
               })
        return products

def parse_shops(category):
    """starts parse shops written in list"""
    products =[]
    #SulpakParsing(), TechnodomParsing(), BeliyVeterParsing()
    shops = [BeliyVeterParsing()]
    for item in shops:
        products.append(item.parse(category))
    return products

def start_parse(categories):
    "Starts parse website with categories in database"
    products = []
    for category in categories:
        products.extend(parse_shops(category))
    return products

