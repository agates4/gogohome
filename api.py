from craigslist import CraigslistHousing
from bs4 import BeautifulSoup
import urllib
from random import randint


class LocationFinder:

    def __init__(self, price, zip_code, query):
        self.cl_h = CraigslistHousing(site='cleveland', area='', category='apa', filters={'max_price': price, 'zip_code': zip_code, 'query': query})

    def find_addresses(self):
        i = 0
        locations = []
        for result in self.cl_h.get_results(sort_by='newest', geotagged=True):
            address = {}
            r = urllib.urlopen(result['url']).read()
            soup = BeautifulSoup(r, "html.parser")
            address_tag = soup.find_all("div", class_="mapaddress")
            if not address_tag:
                pass
            else:
                i = i + 1
                print('--------------------')
                print(address_tag[0].text)
                print(result['price'])
                print(result['name'])
                print(result['url'])
                print('--------------------\n')
                address['address'] = address_tag[0].text
                address['price'] = result['price']
                address['name'] = result['name']
                address['url'] = result['url']
                address['number'] = self.get_phone()
                locations.append(address)
            if i == 3:
                break
        return locations
    
    def get_phone(self):
        f=randint(111,950)
        b=randint(1001,9899)
        a=randint(100,999)
        num="("+str(a)+")-"+str(f)+"-"+str(b)
        z=randint(0,1)
        if (z == 0):
            return ""
        return num 
        


# int , int , string
#loc = LocationFinder(850, 44706, '')
#print(loc.find_addresses())
#print loc.get_phone()
