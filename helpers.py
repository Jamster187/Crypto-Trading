# ALL HELPER FUNCTIONS HERE

import ccxt
import schedule
from config import *

#Exchange initialization
bitfinex = ccxt.bitfinex2()
binance = ccxt.binance()
ftx = ccxt.ftx()
independentreserve = ccxt.independentreserve()


#Exchange API key setup
bitfinex.apiKey = BFXTEST_API_KEY
bitfinex.secret = BFXTEST_SECRET_KEY

#Supported Exchanges

def print_supported_exchanges():
    '''
    Displays a list of supported exchanges, nomenclature to be used in trade
    related functions.
    '''
    for exchange in ccxt.exchanges:
        print(exchange)

#Exchange informational functions

def print_exchange_markets(exchange):
    '''
    Displays a list of available trading pairs for the exchange queried. Valid
    parameters can be found by calling print_supported_exchanges().
    '''
    for market in exchange.load_markets():
        print(market)

def print_exchange_assets(exchange):
    '''
    Displays a list of available assets for the exchange queried. Valid 
    parameters can be found by calling print_supported_exchanges()
    '''
    exchange.load_markets()
    for currency in exchange.currencies:
        print(currency)
    
#Exchange balance helper functions

def get_free_bal(exchange, asset):
    '''
    Gets free balance information for an asset on a specific exchange
    
    exchange = bitfinex, binance, kraken - valid params can be found by
               calling print_supported_exchanges()
    
    asset    = 'BTC', 'ETH', 'USD', 'USDT' - valid params vary by exchange,
               and can be found by calling print_exchange_assets(exchange)
    '''
    return exchange.fetch_balance()['free'][asset]

#Exchange price helper functions

def get_exchange_pair_last(exchange, pair):
    '''
    Gets the last traded price from a market pair on a specific exchange
    
    exchange = bitfinex, binance, kraken - valid params can be found by
               calling print_supported_exchanges()
               
    pair     = 'BTC/USDT', 'ETH/USDT', 'FIDA/USDT' - valid params vary by
             exchange, can be found by calling print_exchange_markets(exchange)
    '''
    return exchange.fetch_ticker(pair)['last']

#Strategy profit settings

minSellProfit = 1.1 #10% above market
minBuyProfit = 0.90  #10% below market

#Exchange action functions (buying, selling, etc)

def get_mm_sell_price(RefExchange, pair):
    '''
    Generates a profitable selling price using RefExchange price data - 
    the "liquid" or "reference" exchange we will be closing arbitrages with.
    
    SupplyExchange = bitfinex, binance, kraken - valid params can be found by
                     calling print_supported_exchanges()
                     
    pair     = 'BTC/USDT', 'ETH/USDT', 'FIDA/USDT' - valid params vary by
             exchange, can be found by calling print_exchange_markets(exchange)
    '''
    return minSellProfit * get_exchange_pair_last(RefExchange, pair)

def get_mm_buy_price(RefExchange, pair):
    '''
    Generates a profitable buying price using RefExchange price data - 
    the "liquid" or "reference" exchange we will be closing arbitrages with.
    
    RefExchange = bitfinex, binance, kraken - valid params can be found by
                     calling print_supported_exchanges()
                     
    pair     = 'BTC/USDT', 'ETH/USDT', 'FIDA/USDT' - valid params vary by
             exchange, can be found by calling print_exchange_markets(exchange)
    '''
    return minBuyProfit * get_exchange_pair_last(RefExchange, pair)

# REVIEW + TEST, PERHAPS CREATE/MODIFY HELPER FUNCTION(S) 4 THE FOLLOWING TASKS:
#
# - When buying an asset, use free balance data + price data to calculate an
#   exact amount to be purchasing
#
# - When setting a price, ensure that the significant digits are respected
#   for that exchange
#
# - When setting an amount, ensure that the significant digits are respected
#   for that exchange

def mm_sellOrder(exchange, targPair, refPair, targAsset):
    '''
    exchange = exchange that we will sell on - valid param can be found by 
               calling print_supported_exchanges()
    targPair = target exchange pair - 'BTC/USDT', 'ETH/USDT', 'TESTBTC/TESTUSDT'
               valid param found by calling print_exchange_markets(exchange)
    refPair = reference pair, 'BTC/USDT', 'ETH/USDT', etc valid param found by
              calling print_exchange_markets(exchange)
    targAsset = asset that will be sold on target exchange 'BTC', 'ETH' - valid
                param can be found by calling print_exchange_assets(exchange)
    '''
    exchange.create_limit_sell_order(targPair, get_free_bal(targAsset), get_mm_sell_price(refPair))

def mm_buyOrder(exchange, targPair, refPair, targAsset):
    '''
    exchange = exchange that we will buy on - valid param can be found by 
               calling print_supported_exchanges()
    targPair = target exchange pair - 'BTC/USDT', 'ETH/USDT', 'TESTBTC/TESTUSDT'
               valid param found by calling print_exchange_markets(exchange)
    refPair = reference pair, 'BTC/USDT', 'ETH/USDT', etc valid param found by
              calling print_exchange_markets(exchange)
    targAsset = asset that'll be expensed on target exchange 'BTC', 'USD'- valid
                param can be found by calling print_exchange_assets(exchange)
    '''    
    exchange.create_limit_buy_order(targPair, ( get_free_bal(targAsset) // get_mm_buy_price(refPair) ), get_mm_buy_price(refPair) )

def testing_price_functions(bnbpair):
    while True:
        print(f"Binance BTC Price : {get_binance_pair_last(bnbpair)} - Min Sell Profit : {minSellProfit} - BFX BTC Offer Price: {get_mm_sell_price(bnbpair)} PROFIT CHECK {get_mm_sell_price(bnbpair)/get_binance_pair_last(bnbpair)}")