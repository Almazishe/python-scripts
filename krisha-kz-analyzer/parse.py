import bs4
import requests
import pandas as pd
import re
import json


class Apartment:
    """
    Apartment representation class
    """
    def __init__(self, link, room_num, price, city, house_year, area):
        self.link = link
        self.room_num = room_num
        self.price = price
        self.city = city
        self.house_year = house_year
        self.area = area

    def to_list(self):
        return [
            self.link,
            self.room_num,
            self.price,
            self.city,
            self.house_year,
            self.area,
        ]

    @staticmethod
    def get_template():
        """
        Dataframe data template
        """
        return {
            'Link': [],
            'RoomNum': [],
            'Price': [],
            'City': [],
            'HouseYear': [],
            'Area': [],
        }



class Client:
    def __init__(self):
        """
        Declare BASE url of website
        """

        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept-Language': 'ru',
        }

        self.base_url = 'https://krisha.kz'

    def load_page(self, url):
        """
        Get string representation of HTML page
        """
        res =  self.session.get(url=url)
        return res.text

    def load_apartments_page(self, page):
        """
        Get list of apartment's string representation on given page
        """
        url = f'{self.base_url}/arenda/kvartiry/?das[_sys.hasphoto]=1&page={page}'
        return self.load_page(url)

    def parse_links_from_page(self, page):
        """
        Get only links of Apartmets
        """
        text = self.load_apartments_page(page)

        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('a.a-card__title')

        # Generate full url of apartment links
        links = list(map(lambda x: self.base_url + x['href'], container))
        return links


    def parse_data_from_apartment_detail_page(self, url):
        """
        Get parsed Apartment class instance
        """


        # Get str representation of apartment detail
        text = self.load_page(url)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Parse number of rooms from title
        title_div = soup.find('div', attrs={'class': 'offer__advert-title'})
        if title_div:
            room_num_str = title_div.find('h1').text.strip()
            room_num_data = room_num_str.split('-')
            room_num = int(room_num_data[0])

        else:
            room_num = None


        # Parse price of apartment
        price_div = soup.find('div', attrs={'class': 'offer__price'})
        try:
            price = int(''.join(price_div.text.split()[:-1]))
        except:
            price = None


        # Parse city of apartment
        city_div = soup.find('div', attrs={'class': 'offer__location offer__advert-short-info'})
        if city_div:
            city_str = city_div.find('span').text
            city_data = city_str.split(',')
            city = city_data[0]
        else:
            city = None


        # Parse house year
        house_year_div = soup.find('div', attrs={'class': 'offer__info-item', 'data-name': 'flat.building'})
        try:
            house_year_str = house_year_div.find('div', attrs={'class': 'offer__advert-short-info'}).text
            house_year = int(re.search(r'\d+', house_year_str).group())
        except:
            house_year = None

        # Parse area of apartment
        area_div = soup.find('div', attrs={'class': 'offer__info-item', 'data-name': 'live.square'})
        if area_div:
            area_str = area_div.find('div', attrs={'class': 'offer__advert-short-info'}).text
            areas = area_str.split()
            area = float(areas[0])
        else:
            area = None

        # Declare Apartment class instance
        apartment = Apartment(url, room_num, price, city, house_year, area)
        return apartment


def generate_links(client, number_of_pages):
    # Get links of apartment details from 1:page_num pages
    links = []
    for i in range(number_of_pages):
        print(i, '/', number_of_pages)
        links.extend(client.parse_links_from_page(i))

    with open('links.txt', 'w') as f:
        f.write(json.dumps(links))

    return links


def read_links():
    """
    Read links saved to txt file
    """
    with open('links.txt', 'r') as f:
        links = json.loads(f.read())

    return links


def save_to_csv(data, portion_num):
    """
    Save data portion to csv
    """

    # Declare dataframe instance with collected data
    df = pd.DataFrame(data, columns=data.keys())

    # Save data to csv file
    df.to_csv (f'apartments_{portion_num}.csv', index = False, header=True)



def main():
    # Declare client isntance
    client = Client()
    links = read_links()

    # Get dataframe data template
    data = Apartment.get_template()

    # Iterate through all links, and collect data of apartment to data template
    length = len(links)
    index = 1
    for i, link in enumerate(links):
        print(link, f'{i}/{length}')
        apartment = client.parse_data_from_apartment_detail_page(link)
        data['Link'].append(apartment.link)
        data['RoomNum'].append(apartment.room_num)
        data['Price'].append(apartment.price)
        data['City'].append(apartment.city)
        data['HouseYear'].append(apartment.house_year)
        data['Area'].append(apartment.area)

        if (i + 1) % 3000 == 0:
            # Divide data by portion of 3000 apartments to not lose all data
            # if some error occur in proccess of parsing
            save_to_csv(data, index)
            index += 1
            data = Apartment.get_template()




if __name__ == '__main__':
    main()



