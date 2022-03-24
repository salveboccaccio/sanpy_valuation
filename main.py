import san
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#To see full dataframe without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#user input
print('enter name of coin - not ticker. i.e. use bitcoin instead of btc')
coin = input('enter name of coin: ')
start = input('Start date in YYYY-MM-DD format: ')
end = input('End date in YYYY-MM-DD format: ')
print('The interval of the returned data - an integer followed by one of: s, m, h, d or w')
t = input('Enter interval: ')

price_df = san.get(
    "ohlc/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#nvt ratio = market cap / transaction volume in usd
tv_df = san.get(
    "volume_usd/"+ coin,
    from_date=start,
    to_date=end,
    interval=t
)

#market cap
mc_df = san.get(
    "marketcap_usd/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#Mayer Multiple: price/200 day moving average
ma_200_df = san.get(
  "price_usd/"+coin,
  from_date=start,
  to_date=end,
  interval=t,
  transform={"type": "moving_average", "moving_average_base": 200},
)

#developer activity
dev_activity_df = san.get(
    "dev_activity/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#daily active addresses
daily_active_addresses_df = san.get(
    "daily_active_addresses/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#transaction volume
transaction_volume_df = san.get(
    "transaction_volume/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#mvrv
mvrv_usd_df = san.get(
    "mvrv_usd/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#token velocity
velocity_df = san.get(
    "velocity/"+coin,
    from_date=start,
    to_date=end,
    interval=t
)

#DF setup for nvt ratio
data = [mc_df, tv_df]
headers = ["market cap", "total volume"]
nvt_ratio = pd.concat(data, axis=1, keys=headers)
nvt_ratio['NVT ratio'] = nvt_ratio['market cap'] / nvt_ratio['total volume']
nvt_ratio = nvt_ratio.drop('market cap', 1)
nvt_ratio = nvt_ratio.drop('total volume', 1)

#DF setup for 7 day moving average nvt
data = [price_df, ma_200_df]
headers = ["daily price", "moving average"]
mm_df = pd.concat(data, axis=1, keys=headers)
nvt_ratio['NVT_7_DAY'] = nvt_ratio['NVT ratio'].rolling(window = 7).mean()

nvt_7_day = nvt_ratio['NVT_7_DAY']
nvt_ratio_chart = nvt_ratio['NVT ratio']

fig, axs = plt.subplots(2, 1, figsize=(14, 9))

#NVT Ratio plotting
axs[0].plot(nvt_ratio_chart)
axs[0].set_title('NVT Ratio')
axs[0].set_ylabel('NVT')
axs[0].set_xlabel('Time')

#7 day moving average NVT plotting
axs[1].plot(nvt_7_day)
axs[1].set_title('7 day moving average NVT')
axs[1].set_ylabel('NVT')
axs[1].set_xlabel('Time')

fig.canvas.manager.set_window_title('NVT Data')
fig.tight_layout()


fig2, axs = plt.subplots(3, 1, figsize=(16, 9))

#daily active addresses plotting
axs[0].plot(daily_active_addresses_df)
axs[0].set_title('Daily Active Addresses')
axs[0].set_ylabel('Daily Active Addresses')
axs[0].set_xlabel('Time')

#Transaction Volume Plotting
axs[1].plot(transaction_volume_df)
axs[1].set_title(' Transaction Volume')
axs[1].set_ylabel('Transaction Volume')
axs[1].set_xlabel('Time')

#Developer activity plotting
axs[2].plot(dev_activity_df)
axs[2].set_title('Developer activity')
axs[2].set_ylabel('Developer Activity')
axs[2].set_xlabel('Time')

fig2.canvas.manager.set_window_title('Usage Statistic')
fig2.tight_layout()


fig3, axs = plt.subplots(2, 1, figsize=(14, 9))

#MVRV plotting
axs[0].plot(mvrv_usd_df)
axs[0].set_title('MVRV (USD)')
axs[0].set_ylabel('MVRV')
axs[0].set_xlabel('Time')

#Token Velocity
axs[1].plot(velocity_df)
axs[1].set_title('Token Velocity')
axs[1].set_ylabel('Token Velocity')
axs[1].set_xlabel('Time')

fig3.canvas.manager.set_window_title('MVRV and Token Velocity')
fig3.tight_layout()

plt.show()
