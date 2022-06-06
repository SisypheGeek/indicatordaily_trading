import pandas as pd
import requests
from bs4 import BeautifulSoup


def soup_param(website):
    header = {
        "User-Agent": 'Mozilla/5.0',
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        }

    # website = 'https://www.coingecko.com/en'
    response = requests.get(website, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    num_page2 = soup.find_all('li', {'class': 'page-item'})
    total_page = int(num_page2[len(num_page2)-2].text)
    return header, total_page


def get_table(url, header, total_page):
    tables = []
    for i in range(1, total_page):
        # print(i)
        # website
        website = url + 'en?page=' + str(i)
        # request to website
        response = requests.get(website, headers=header)
        # soup object
        soup = BeautifulSoup(response.content, 'html.parser')
        tables.append(pd.read_html(str(soup))[0])
    master_table = pd.concat(tables)
    master_table = master_table[['#', 'Coin', 'Price', '1h', '24h', '7d', '24h Volume', 'Mkt Cap']]
    return master_table


def main():
    url = 'https://www.coingecko.com/'
    header, total_page = soup_param(url)
    master_table = get_table(url, header, total_page)
    master_table.rename(columns={'#': 'Rank', 'Coin': 'Token', 'Price': 'Today Price', '1h': 'Change(1h)', '24h': 'Change(24h)', '7d': 'Change(7d)', '24h Volume': 'Volume(24h)', 'Mkt Cap': 'Market Cap'}, inplace=True)
    master_table['Symbol'] = master_table['Token'].apply(lambda x: x.split()[-1])
    master_table = master_table[['Symbol', 'Rank', 'Today Price', 'Change(1h)', 'Change(24h)', 'Change(7d)', 'Volume(24h)', 'Market Cap']]
    return master_table


if __name__ == "__main__":
    master_table = main()
