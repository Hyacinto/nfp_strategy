import pandas as pd

def data_from_an_intervall(df, dates):

    df_dates = df["DateTime"].dt.date

    dates["Date"] = pd.to_datetime(dates["Date"]).dt.date
    dates = dates[dates["Date"].isin(df_dates)]

    intervals = []
    
    for _, row in dates.iterrows():
        date = row["Date"]
        start = row["Time"]
       
        start_time = pd.Timestamp(f"{date} {start}:15:00", tz="UTC")
   
        end_time = pd.Timestamp(f"{date} {start + 1}:45:00", tz="UTC")
  
        df_interval = df[(df["DateTime"] >= start_time) & (df["DateTime"] <= end_time)]
        intervals.append(df_interval)

    return pd.concat(intervals)

df = pd.read_csv("../data/nfp_eurusd_with_indicators.csv", parse_dates=['DateTime'])
dates = pd.read_csv("../data/nfp_dates.csv")

filtered_df = data_from_an_intervall(df, dates)

filtered_df.to_csv("../data/nfp_eurusd_with_indicators.csv", index=False)
