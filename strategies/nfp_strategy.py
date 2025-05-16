import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta
import pytz

# NFP dátumok betöltése
nfp_dates = pd.read_csv('data/nfp_dates.csv')
nfp_dates['Date'] = pd.to_datetime(nfp_dates['Date']).dt.date

# Backtest eredmények betöltése
df = pd.read_csv('data/nfp_eurusd_with_indicators.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date'] = df['DateTime'].dt.date

st.title('NFP News Trading _Robot_ - For-If-Else Based Backtest')

# Kereskedési napok kiválasztása
trading_days = df['Date'].unique()
choosen_day = st.selectbox('Please choose a trading day:', trading_days)

if choosen_day:
    st.subheader(f'Trading day: {choosen_day}')
    daily_data = df[df['Date'] == choosen_day].copy() 
    nfp_time = f"{nfp_dates[nfp_dates['Date'] == choosen_day]['Time'].values[0]}:30"
    nfp_datetime = datetime.strptime(f"{choosen_day} {nfp_time}", '%Y-%m-%d %H:%M')  

    daily_data['DateTime'] = daily_data['DateTime'].dt.tz_convert('UTC')
    nfp_datetime = nfp_datetime.replace(tzinfo=pytz.UTC)  

    # Vizualizáció gyertyákkal és indikátorokkal
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=daily_data['DateTime'],
                                 open=daily_data['open'],
                                 high=daily_data['high'],
                                 low=daily_data['low'],
                                 close=daily_data['close'],
                                 name='Price'))
    fig.add_trace(go.Scatter(x=daily_data['DateTime'], y=daily_data['SMA_20'], mode='lines', name='SMA 20'))
    fig.add_trace(go.Scatter(x=daily_data['DateTime'], y=daily_data['SMA_50'], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=daily_data['DateTime'], y=daily_data['BB_high'], mode='lines', name='Bollinger Upper'))
    fig.add_trace(go.Scatter(x=daily_data['DateTime'], y=daily_data['BB_low'], mode='lines', name='Bollinger Lower'))

    # NFP időpont jelölése
    fig.add_trace(go.Scatter(x=[nfp_datetime], y=[daily_data['close'].iloc[0]],
                             mode='markers+text', text=['NFP'],
                             textposition='bottom center',
                             marker=dict(color='red', size=10), name='NFP announcement'))

    # Stratégia: Belépési feltételek és Buy/Sell Bracket
    position = None
    entry_price = 0
    stop_loss = 0
    take_profit = 0
    total_profit = 0

    # Kereskedési információk tárolása
    trade_log = []

    for i, row in daily_data.iterrows(): # Minden soron végigmegyünk a DataFrame-en
        current_time = row['DateTime']

        # Long belépési feltételek
        if position is None and row['RSI'] < 30 and row['close'] < row['BB_low']:
            position = 'long'
            entry_price = row['close']
            trade_log.append(f"⏰ **{current_time}**: Long position opened, Entry = {entry_price:.5f}")
            # Belépési pont jelölése (zöld pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[entry_price],
                           mode='markers', marker=dict(color='green', size=10),
                           name='Long Entry'))
            # Nyíl a pozíció irányába
            fig.add_annotation(x=current_time, y=entry_price, text='⬆️', showarrow=False, font=dict(size=15))

        # Short belépési feltételek
        elif position is None and row['RSI'] > 70 and row['close'] > row['BB_high']:
            position = 'short'
            entry_price = row['close']
            trade_log.append(f"⏰ **{current_time}**: Short position opened, Entry = {entry_price:.5f}")
            # Belépési pont jelölése (piros pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[entry_price],
                           mode='markers', marker=dict(color='red', size=10),
                           name='Short Entry'))
            # Nyíl a pozíció irányába
            fig.add_annotation(x=current_time, y=entry_price, text='⬇️', showarrow=False, font=dict(size=15))

        # Kilépési feltételek
        if position == 'long' and current_time >= nfp_datetime + timedelta(hours=1):
            profit = row['close'] - entry_price
            total_profit += profit
            position = None
            trade_log.append(f"✅ **{current_time}**: Long position closed, Close at = {row['close']:.5f}, Profit = {profit:.5f}")
            # Kilépési pont jelölése (kék pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[row['close']],
                           mode='markers', marker=dict(color='blue', size=10),
                           name='Long Exit'))

        elif position == 'short' and current_time >= nfp_datetime + timedelta(hours=1):
            profit = entry_price - row['close']
            total_profit += profit
            position = None
            trade_log.append(f"✅ **{current_time}**: Short position closed, Close at = {row['close']:.5f}, Profit = {profit:.5f}")
            # Kilépési pont jelölése (narancssárga pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[row['close']],
                           mode='markers', marker=dict(color='orange', size=10),
                           name='Short Exit'))

    # Kereskedési információk megjelenítése
    st.subheader("Trade Information")
    for log in trade_log:
        st.markdown(log)

    # Összesített profit megjelenítése
    st.subheader("Total Results")
    st.write(f"📊 **Total Profit**: {total_profit:.5f}")

    # Grafikon megjelenítése
    fig.update_layout(title=f'Trading Day: {choosen_day}', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)