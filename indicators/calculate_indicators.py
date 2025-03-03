import pandas as pd
import ta

def calculate_indicators_for_each_nfp(df: pd.DataFrame) -> pd.DataFrame:
    all_data = []

    # Szétválasztás dátum szerint
    for _, group in df.groupby(df['DateTime'].dt.date):
        # Rendezés időrendben, ha szükséges
        group = group.sort_index()

        # Indikátorok kiszámítása a csak erre a dátumra vonatkozó két órás adatokra
        group['SMA_20'] = ta.trend.sma_indicator(group['close'], window=20)
        group['SMA_50'] = ta.trend.sma_indicator(group['close'], window=50)
        group['EMA_20'] = ta.trend.ema_indicator(group['close'], window=20)

        group['RSI'] = ta.momentum.rsi(group['close'], window=14)
        group['ATR'] = ta.volatility.average_true_range(group['high'], group['low'], group['close'], window=14)

        bb = ta.volatility.BollingerBands(group['close'], window=20, window_dev=2)
        group['BB_high'] = bb.bollinger_hband()
        group['BB_low'] = bb.bollinger_lband()

        macd = ta.trend.MACD(group['close'], window_slow=26, window_fast=12, window_sign=9)
        group['MACD'] = macd.macd()
        group['MACD_signal'] = macd.macd_signal()
        group['MACD_diff'] = macd.macd_diff()

        all_data.append(group)
    
    # Az összes részhalmaz egyesítése
    return pd.concat(all_data, ignore_index=True)

nfp_eurusd = pd.read_csv("../data/nfp_eurusd.csv", parse_dates=['DateTime'])

# Indikátorszámítás a szétválasztott adatokra
nfp_eurusd_with_indicators = calculate_indicators_for_each_nfp(nfp_eurusd)

nfp_eurusd_with_indicators.to_csv('../data/nfp_eurusd_with_indicators.csv', index=False)


