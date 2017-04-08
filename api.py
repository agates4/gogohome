from craigslist import CraigslistHousing
from bs4 import BeautifulSoup
import urllib


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
            print(address_tag)
            if not address_tag:
                print("no address found")
            else:
                i = i + 1
                print(address_tag[0].text)
                print(result['price'])
                print(result['name'])
                print(result['url'])
                address['address'] = address_tag[0].text
                address['price'] = result['price']
                address['name'] = result['name']
                address['url'] = result['url']
                locations.append(address)
            if i == 3:
                break
        return locations


# int , int , string
# loc = LocationFinder(850, 44110, 'bus')
# print(loc.find_addresses())
