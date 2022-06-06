import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


def get_source(driver_path, website):
    driver = webdriver.Chrome(driver_path)
    driver.get(website)
    sleep(3)
    source = driver.page_source
    return source


def get_table_bs(driver_path, urls):
    source_best = get_source(driver_path, urls['Best'])
    source_good = get_source(driver_path, urls['Good'])
    soup_best = BeautifulSoup(source_best, 'html.parser')
    soup_good = BeautifulSoup(source_good, 'html.parser')
    table_best = soup_best.find('table', class_="CryptoTable_table__P2T2N")
    table_good = soup_good.find('table', class_="CryptoTable_table__P2T2N")
    return table_best, table_good


def selected_data_dic(table):
    retrieved_data = {}
    for c in table.find_all('tbody'):
        rows = c.find_all('tr', {'class': lambda value: value and value.startswith('CryptoTable')})
        for row in rows:
            symbol = row.find('a').text
            # print(symbol)
            rank = row.find('strong').text
            price = row.find_all('div', {'class': 'right'})[0].text
            price_ath = row.find_all('div', {'class': 'right'})[1].text
            change_24 = row.find_all('div', {'class': lambda value: value and value.startswith('center Percent')})[
                0].text
            change_30 = row.find_all('div', {'class': lambda value: value and value.startswith('center Percent')})[
                1].text
            change_ath = row.find_all('div', {'class': lambda value: value and value.startswith('center Percent')})[
                2].text
            retrieved_data[symbol] = {'Price': price,
                                      'Price ATH': price_ath,
                                      'Rank': rank,
                                      'Change(24H)': change_24,
                                      'Change(30D)': change_30,
                                      'Change(ATH)': change_ath
                                       }
    return retrieved_data


def main():
    base_url = 'https://4kings.xyz/crypto'
    urls = {'Best': base_url + '/best',
            'Good': base_url + '/good'}
    driver_path = '/Users/thomasgrandguillot/Desktop/chromedriver'
    table_best, table_good = get_table_bs(driver_path, urls)
    data_best_dic = selected_data_dic(table_best)
    data_good_dic = selected_data_dic(table_good)
    df_best = pd.DataFrame.from_dict(data_best_dic, orient='index')
    df_good = pd.DataFrame.from_dict(data_good_dic, orient='index')
    return df_best, df_good


if __name__ == "__main__":
    df_best, df_good = main()
