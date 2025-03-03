import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta
import pytz

# NFP dátumok betöltése
nfp_dates = pd.read_csv('../data/nfp_dates.csv')
nfp_dates['Date'] = pd.to_datetime(nfp_dates['Date']).dt.date

# Backtest eredmények betöltése
df = pd.read_csv('../data/nfp_eurusd_with_indicators.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date'] = df['DateTime'].dt.date

st.title('NFP Hírkereskedő Robot Eredmények - For-If-Else Alapú Backtest')

# Kereskedési napok kiválasztása
kereskedesi_napok = df['Date'].unique()
kivalasztott_nap = st.selectbox('Válassz egy kereskedési napot:', kereskedesi_napok)

if kivalasztott_nap:
    st.subheader(f'Kereskedési nap: {kivalasztott_nap}')
    napi_adatok = df[df['Date'] == kivalasztott_nap].copy() 
    nfp_time = f"{nfp_dates[nfp_dates['Date'] == kivalasztott_nap]['Time'].values[0]}:30"
    nfp_datetime = datetime.strptime(f"{kivalasztott_nap} {nfp_time}", '%Y-%m-%d %H:%M')  

    napi_adatok['DateTime'] = napi_adatok['DateTime'].dt.tz_convert('UTC')
    nfp_datetime = nfp_datetime.replace(tzinfo=pytz.UTC)  

    # Vizualizáció gyertyákkal és indikátorokkal
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=napi_adatok['DateTime'],
                                 open=napi_adatok['open'],
                                 high=napi_adatok['high'],
                                 low=napi_adatok['low'],
                                 close=napi_adatok['close'],
                                 name='Price'))
    fig.add_trace(go.Scatter(x=napi_adatok['DateTime'], y=napi_adatok['SMA_20'], mode='lines', name='SMA 20'))
    fig.add_trace(go.Scatter(x=napi_adatok['DateTime'], y=napi_adatok['SMA_50'], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=napi_adatok['DateTime'], y=napi_adatok['BB_high'], mode='lines', name='Bollinger Upper'))
    fig.add_trace(go.Scatter(x=napi_adatok['DateTime'], y=napi_adatok['BB_low'], mode='lines', name='Bollinger Lower'))

    # NFP időpont jelölése
    fig.add_trace(go.Scatter(x=[nfp_datetime], y=[napi_adatok['close'].iloc[0]],
                             mode='markers+text', text=['NFP'],
                             textposition='bottom center',
                             marker=dict(color='red', size=10), name='NFP Kiadás'))

    # Stratégia: Belépési feltételek és Buy/Sell Bracket
    position = None
    entry_price = 0
    stop_loss = 0
    take_profit = 0
    total_profit = 0

    # Kereskedési információk tárolása
    trade_log = []

    for i, row in napi_adatok.iterrows():
        current_time = row['DateTime']

        # Long belépési feltételek
        if position is None and row['RSI'] < 30 and row['close'] < row['BB_low']:
            position = 'long'
            entry_price = row['close']
            trade_log.append(f"⏰ **{current_time}**: Long pozíció létrehozva, Belépés = {entry_price:.5f}")
            # Belépési pont jelölése (zöld pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[entry_price],
                           mode='markers', marker=dict(color='green', size=10),
                           name='Long Belépés'))
            # Nyíl a pozíció irányába
            fig.add_annotation(x=current_time, y=entry_price, text='⬆️', showarrow=False, font=dict(size=15))

        # Short belépési feltételek
        elif position is None and row['RSI'] > 70 and row['close'] > row['BB_high']:
            position = 'short'
            entry_price = row['close']
            trade_log.append(f"⏰ **{current_time}**: Short pozíció létrehozva, Belépés = {entry_price:.5f}")
            # Belépési pont jelölése (piros pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[entry_price],
                           mode='markers', marker=dict(color='red', size=10),
                           name='Short Belépés'))
            # Nyíl a pozíció irányába
            fig.add_annotation(x=current_time, y=entry_price, text='⬇️', showarrow=False, font=dict(size=15))

        # Kilépési feltételek
        if position == 'long' and current_time >= nfp_datetime + timedelta(hours=1):
            profit = row['close'] - entry_price
            total_profit += profit
            position = None
            trade_log.append(f"✅ **{current_time}**: Long pozíció lezárva, Záróár = {row['close']:.5f}, Profit = {profit:.5f}")
            # Kilépési pont jelölése (kék pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[row['close']],
                           mode='markers', marker=dict(color='blue', size=10),
                           name='Long Kilépés'))

        elif position == 'short' and current_time >= nfp_datetime + timedelta(hours=1):
            profit = entry_price - row['close']
            total_profit += profit
            position = None
            trade_log.append(f"✅ **{current_time}**: Short pozíció lezárva, Záróár = {row['close']:.5f}, Profit = {profit:.5f}")
            # Kilépési pont jelölése (narancssárga pötty)
            fig.add_trace(go.Scatter(x=[current_time], y=[row['close']],
                           mode='markers', marker=dict(color='orange', size=10),
                           name='Short Kilépés'))

    # Kereskedési információk megjelenítése
    st.subheader("Kereskedési információk")
    for log in trade_log:
        st.markdown(log)

    # Összesített profit megjelenítése
    st.subheader("Összesített eredmény")
    st.write(f"📊 **Összesített profit**: {total_profit:.5f}")

    # Grafikon megjelenítése
    fig.update_layout(title=f'Kereskedési nap: {kivalasztott_nap}', xaxis_title='Dátum', yaxis_title='Ár')
    st.plotly_chart(fig)