import pandas as pd
import os
import glob

# Automatically find all bhavcopy CSV files in current folder
files = glob.glob("BhavCopy_NSE_CM_*.csv")
print(f"Found files: {files}")

all_data = []

for file in files:
    df = pd.read_csv(file)
    df = df[["TradDt", "TckrSymb", "SctySrs", "OpnPric", "HghPric", "LwPric", "ClsPric", "TtlTradgVol"]]
    df.columns = ["DATE", "SYMBOL", "SERIES", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    df = df[df["SERIES"] == "EQ"]
    all_data.append(df)

# Combine all days into one table
df = pd.concat(all_data, ignore_index=True)

# Fix date and drop missing
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.dropna()

# Sort by symbol and date
df = df.sort_values(["SYMBOL", "DATE"])

# Daily Return
df["DAILY_RETURN"] = (df["CLOSE"] - df["OPEN"]) / df["OPEN"]

print(f"Total records: {len(df)}")
print(df.head(5))

# 7-day Moving Average (per stock)
df["MA_7"] = df.groupby("SYMBOL")["CLOSE"].transform(
    lambda x: x.rolling(7).mean()
)

# 52-week High and Low (per stock)
df["52W_HIGH"] = df.groupby("SYMBOL")["HIGH"].transform("max")
df["52W_LOW"] = df.groupby("SYMBOL")["LOW"].transform("min")

# Volatility Score (your custom metric — this will impress them)
df["VOLATILITY"] = df.groupby("SYMBOL")["DAILY_RETURN"].transform("std")

print(df[["SYMBOL", "DATE", "CLOSE", "MA_7", "52W_HIGH", "52W_LOW", "VOLATILITY"]].head(10))

df.to_csv("clean_data.csv", index=False)
print("Saved to clean_data.csv ✅")