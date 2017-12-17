'''
from zipline.api import order, record, symbol
from zipline.algorithm import TradingAlgorithm
def initialize(context):
   pass

def handle_data(context, data):
  order(symbol('AAPL'), 10)
  record(AAPL=data.current(symbol('AAPL'), 'price'))

algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
'''
import pytz
import pandas as pd
from datetime import datetime
from zipline.api import order, symbol, record, order_target
from zipline.algorithm import TradingAlgorithm
#from zipline.utils.factory import load_bars_from_yahoo
#import pyexcel
from collections import OrderedDict 
# Load data manually from Yahoo! finance
start = pd.Timestamp("2015-4-1", tz='UTC')#datetime(2011, 1, 1, 0, 0, 0, 0, pytz.utc).date()
end = pd.Timestamp("2015-12-30", tz='UTC')#datetime(2012,1,1,0,0,0,0, pytz.utc).date()

data = OrderedDict()
data['SPY'] = pd.read_csv('aapl-2015-google.csv', index_col=0, parse_dates=['Date'])
df= data['SPY']
print data['SPY'].head()
type(data['SPY'])

panel = pd.Panel(data)
panel.minor_axis = ['open', 'high', 'low', 'close', 'volume']
panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
#data = load_bars_from_yahoo(stocks=['SPY'], start=start,end=end)
#code
def initialize(context):
    context.security = symbol('SPY')


def handle_data(context, data):
    order(context.security, 10)
    record(AAPL=data.current(context.security, 'price'))
'''
#code
def handle_data(context, data):
    MA1 = data[context.security].mavg(10)
    MA2 = data[context.security].mavg(20)
    date = str(data[context.security].datetime)[:10]
    current_price = data[context.security].price
    current_positions = context.portfolio.positions[symbol('SPY')].amount
    cash = context.portfolio.cash
    value = context.portfolio.portfolio_value
    current_pnl = context.portfolio.pnl

    #code (this will come under handle_data function only)
    if (MA1 > MA2) and current_positions == 0:
        number_of_shares = int(cash/current_price)
        order(context.security, number_of_shares)
        record(date=date,MA1 = MA1, MA2 = MA2, Price= 
    current_price,status="buy",shares=number_of_shares,PnL=current_pnl,cash=cash,value=value)

    elif (MA1 < MA2) and current_positions != 0:
         order_target(context.security, 0)
         record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="sell",shares="--",PnL=current_pnl,cash=cash,value=value)

    else:
        record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="--",shares="--",PnL=current_pnl,cash=cash,value=value)
'''


def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('AAPL price (USD)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()
algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data, capital_base = 100000.0,start = start, end = end , analyze=analyze)
#run algo                         #run algo
perf_manual = algo_obj.run(panel) 
'''
algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data, capital_base = 100000.0,start = start, end = end , analyze=analyze, )
#run algo                         #run algo
perf_manual= algo_obj.run()
'''
#perf_manual[["MA1","MA2","Price"]].plot()
perf_manual.head()

