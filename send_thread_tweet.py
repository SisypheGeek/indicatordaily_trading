import sys
sys.path.insert(len(sys.path), '/Users/thomasgrandguillot/Documents/GitHub/twitter_bot')
import tweet_bot

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



api = tweet_bot.main_connection()