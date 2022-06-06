import pandas as pd
import investpy
import requests
from bs4 import BeautifulSoup
import coingecko_webscraping
import fourking_webscrap
from datetime import datetime
# indices = investpy.indices.get_indices()


def get_indices():
    us_ind_overview = investpy.indices.get_indices_overview(country='united states', n_results=1000)
    us_ind_overview = us_ind_overview[us_ind_overview['name'].isin(['Dow Jones', 'Nasdap 100', 'S&P 500', 'US Dollar Index'])]
    us_ind_overview = us_ind_overview[['country', 'name', 'last', 'change_percentage','currency']]
    eur_ind_overview = investpy.indices.get_indices_overview(country='germany')
    eur_ind_overview = eur_ind_overview[eur_ind_overview['name'].isin(['DAX', 'Euro Stoxx 50'])]
    eur_ind_overview = eur_ind_overview[['country', 'name', 'last', 'change_percentage','currency']]
    jap_ind_overview = investpy.indices.get_indices_overview(country='japan')
    jap_ind_overview = jap_ind_overview[jap_ind_overview['name'].isin(['Nikkei 225'])]
    jap_ind_overview = jap_ind_overview[['country', 'name', 'last', 'change_percentage','currency']]
    uk_ind_overview = investpy.indices.get_indices_overview(country='united kingdom')
    uk_ind_overview = uk_ind_overview[uk_ind_overview['name'].isin(['FTSE 100'])]
    uk_ind_overview = uk_ind_overview[['country', 'name', 'last', 'change_percentage','currency']]
    all_indices = pd.concat([us_ind_overview, eur_ind_overview, jap_ind_overview, uk_ind_overview])
    # all_indices = all_indices.set_index('name')
    return all_indices

def get_cmd():
    cmd_metal = investpy.commodities.get_commodities_overview(group='metals')
    cmd_metal = cmd_metal[cmd_metal['name'].isin(['Gold', 'Silver'])]
    cmd_metal = cmd_metal[['country', 'name', 'last', 'change_percentage','currency']]
    cmd_energy = investpy.commodities.get_commodities_overview(group='energy')
    cmd_energy = cmd_energy[cmd_energy['name'].isin(['Brent Oil', 'Crude Oil WTI', 'Natural Gas'])]
    cmd_energy = cmd_energy[['country', 'name', 'last', 'change_percentage','currency']]
    all_cmd = pd.concat([cmd_metal, cmd_energy])
    # all_cmd = all_cmd.set_index('name')
    return all_cmd

def get_fx():
    fx = investpy.currency_crosses.get_currency_crosses_overview('usd', as_json=False, n_results=100)
    fx = fx[fx['name'].isin(['EUR/USD - Euro US Dollar', 'GBP/USD - British Pound US Dollar'])]
    fx = fx[['symbol', 'name', 'bid', 'change_percentage']]
    # fx = fx.set_index('name')
    return fx

def get_calendar():
    datacalendar = investpy.economic_calendar()
    datacalendar = datacalendar[datacalendar['importance'].isin(['medium', 'high'])][
        ['date', 'time', 'zone', 'importance', 'event', 'actual', 'forecast', 'previous']]
    return datacalendar

def get_bond():
    bond_us = investpy.bonds.get_bonds_overview('united states')
    bond_ger = investpy.bonds.get_bonds_overview('germany')
    bond_uk = investpy.bonds.get_bonds_overview('united kingdom')
    dic_bond = {'us': bond_us['last_close'], 'uk': bond_uk['last_close'], 'ger': bond_ger['last_close']}
    info_bond_us10 = investpy.bonds.get_bond_information(bond='U.S. 10Y')
    info_bond_us10 =info_bond_us10[['Bond Name', 'Maturity Date', 'Price', 'Coupon']]
    info_bond_us10['change_percentage'] = bond_us[bond_us['name']=='U.S. 10Y']['change_percentage'].values[0]
    # info_bond_us10 = info_bond_us10.set_index('Bond Name')
    info_bond_ger10 = investpy.bonds.get_bond_information(bond='Germany 10Y')
    info_bond_ger10 =info_bond_ger10[['Bond Name', 'Maturity Date', 'Price', 'Coupon']]
    info_bond_ger10['change_percentage'] = bond_ger[bond_ger['name']=='Germany 10Y']['change_percentage'].values[0]
    # info_bond_ger10 = info_bond_ger10.set_index('Bond Name')
    info_bond_ger5 = investpy.bonds.get_bond_information(bond='Germany 5Y')
    info_bond_ger5 =info_bond_ger5[['Bond Name', 'Maturity Date', 'Price', 'Coupon']]
    info_bond_ger5['change_percentage'] = bond_ger[bond_ger['name']=='Germany 5Y']['change_percentage'].values[0]
    # info_bond_ger5 = info_bond_ger5.set_index('Bond Name')
    info_bond_uk = investpy.bonds.get_bond_information(bond='U.K. 10Y')
    info_bond_uk =info_bond_uk[['Bond Name', 'Maturity Date', 'Price', 'Coupon']]
    info_bond_uk['change_percentage'] = bond_uk[bond_uk['name']=='U.K. 10Y']['change_percentage'].values[0]
    # info_bond_uk = info_bond_uk.set_index('Bond Name')
    all_bond = pd.concat([info_bond_us10, info_bond_ger10, info_bond_ger5, info_bond_uk])
    return all_bond, dic_bond


def get_crypto():
    header = {
        "User-Agent": 'Mozilla/5.0',
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    url = 'https://www.investing.com/crypto/currencies'
    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    ccy = soup.find('table',
                    class_="genTbl openTbl js-all-crypto-table mostActiveStockTbl crossRatesTbl allCryptoTlb wideTbl elpTbl elp15")
    ccy_dic = {}
    for c in ccy.find_all('tbody'):
        rows = c.find_all('tr')
        for row in rows:
            symbol = row.find('td', class_='left noWrap elp symb js-currency-symbol').text.strip()
            rank = row.find('td', class_='rank icon').text.strip()
            mar_cap = row.find('td', class_='js-market-cap').text.strip()
            price_usd = row.find('td', class_='price js-currency-price').text.strip()
            vol_24 = row.find('td', class_='js-24h-volume').text.strip()
            change_1d = row.find('td', class_=lambda value: value and value.startswith('js-currency-change-24h')).text.strip()
            change_7d = row.find('td', class_=lambda value: value and value.startswith('js-currency-change-7d')).text.strip()
            ccy_dic[symbol] = {'Rank': rank,
                               'Price': price_usd,
                               'Markey Cap': mar_cap,
                               'Volume last 24h':  vol_24,
                               'Change(24h)': change_1d,
                               'Change(7d)': change_7d
                               }
    ccy_df = pd.DataFrame.from_dict(ccy_dic, orient='index')
    return ccy_df


def get_crypto_select_list(all_coin_df):
    blueschips_list = ['BTC', 'ETH']
    stable_coin_list = ['USDT', 'USDC', 'BUSD', 'TUSD', 'USDP']
    forked_coins = ['ETC', 'BCH']
    dex_stable_coin = ['DAI', 'FRAX', 'UST']
    eth_comp = ['AVAX', 'SOL', 'DOT', 'COSMOS', 'NEAR', 'ADA', 'ALGO', 'XTZ', 'EGLD']
    defi_coin = ['AAVE', 'UNI', 'CAKE']
    eth_scaling_sol = ['MATIC']
    cex_token = ['FTT', 'CRO', 'GT', 'KCS', 'BNB']
    defi_token = ['AAVE', 'UNI', 'COMP', 'XRP']
    meta_token = ['SAND', 'APE', 'MANA']
    meme_token = ['DOGE', 'SHIB']
    stake_token = ['STETH']
    wrapped_token = ['WBTC']
    spe_app_token = ['LINK', 'LTC']
    select_coin = blueschips_list + stable_coin_list + forked_coins + dex_stable_coin + eth_comp + defi_coin + eth_scaling_sol + cex_token + defi_token + meta_token + meme_token + stake_token + wrapped_token + spe_app_token
    select_crypto_df = all_coin_df[all_coin_df['Symbol'].isin(select_coin)]
    select_crypto_df = select_crypto_df.iloc[:38, :]
    return select_crypto_df


def write_excel(all_indices, all_bond, fx, all_cmd, datacalendar, select_crypto_df, df_best):
    row = 3
    start_title = row + len(all_indices) + 2 + len(all_bond) + 2 + len(fx) + 2 + len(all_cmd) + 2 + len(
        datacalendar) + 2 + len(select_crypto_df) + 2
    text = 'Today 5 Tokens to watch with respect to the method explain in the email'

    # with pd.ExcelWriter('Overnight_Market_Data_Thomas.xlsx') as writer:
    writer = pd.ExcelWriter("/Users/thomasgrandguillot/Documents/GitHub/indicatordaily_trading/output/Overnight_Market_Pulse_" + datetime.today().strftime('%Y%m%d') + ".xlsx",
                            engine="xlsxwriter")
    all_indices.to_excel(writer, sheet_name='Market_Data', startrow=row, index=False)
    all_bond.to_excel(writer, sheet_name='Market_Data', startrow=row + len(all_indices) + 2, index=False)
    fx.to_excel(writer, sheet_name='Market_Data', startrow=row + len(all_indices) + 2 + len(all_bond) + 2, index=False)
    all_cmd.to_excel(writer, sheet_name='Market_Data',
                     startrow=row + len(all_indices) + 2 + len(all_bond) + 2 + len(fx) + 2, index=False)
    try:
        datacalendar.to_excel(writer, sheet_name='Market_Data',
                              startrow=row + len(all_indices) + 2 + len(all_bond) + 2 + len(fx) + 2 + len(all_cmd) + 2,
                              index=False)
    except AttributeError:
        pass
    select_crypto_df.to_excel(writer, sheet_name='Market_Data',
                              startrow=row + len(all_indices) + 2 + len(all_bond) + 2 + len(fx) + 2 + len(
                                  all_cmd) + 2 + len(datacalendar) + 2, index=False)
    df_best.iloc[:5, :].reset_index().rename(columns={'index': 'symbol'}).to_excel(writer, sheet_name='Market_Data',
                                                                                   startrow=row + len(
                                                                                       all_indices) + 2 + len(
                                                                                       all_bond) + 2 + len(
                                                                                       fx) + 2 + len(all_cmd) + 2 + len(
                                                                                       datacalendar) + 2 + len(
                                                                                       select_crypto_df) + 3,
                                                                                   index=False)
    worksheet = writer.sheets['Market_Data']
    worksheet.write(start_title, 0, text)
    writer.save()


def main():
    all_bond, dic_bond = get_bond()
    print('Extract Bond overnight market data.')
    fx = get_fx()
    print('Extract FX overnight market data.')
    all_indices = get_indices()
    print('Extract Indices overnight market data.')
    all_cmd = get_cmd()
    print('Extract Commodity overnight market data.')
    try:
        datacalendar = get_calendar()
    except KeyError:
        datacalendar = 'No important event for the day.'
    print('Extract Economic calendar for the day.')
    all_coin_df = coingecko_webscraping.main()
    print('Extract Crypto overnight market data.')
    df_best, df_good = fourking_webscrap.main()
    print('Extract Best overnight coin market data')
    select_crypto_df = get_crypto_select_list(all_coin_df)
    write_excel(all_indices, all_bond, fx, all_cmd, datacalendar, select_crypto_df, df_best)
    return all_bond, dic_bond, fx, all_indices, all_cmd, datacalendar, all_coin_df, df_best, df_good, select_crypto_df


if __name__ == '__main__':
    all_bond, dic_bond, fx, all_indices, all_cmd, datacalendar, all_coin_df, df_best, df_good, select_crypto_df = main()


