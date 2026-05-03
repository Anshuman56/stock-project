import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

df = pd.read_csv("clean_data.csv")

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/companies")
def get_companies():
    symbols = df["SYMBOL"].unique().tolist()
    return {"companies": symbols}

@app.get("/data/{symbol}")
def get_stock_data(symbol: str):
    stock = df[df["SYMBOL"] == symbol.upper()]
    data = stock.tail(30).fillna(0)
    return {"data": data.to_dict(orient="records")}

@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    stock = df[df["SYMBOL"] == symbol.upper()].fillna(0)
    return {
        "symbol": symbol.upper(),
        "52w_high": stock["52W_HIGH"].max(),
        "52w_low": stock["52W_LOW"].min(),
        "avg_close": round(stock["CLOSE"].mean(), 2)
    }

@app.get("/compare")
def compare_stocks(symbol1: str, symbol2: str):
    stock1 = df[df["SYMBOL"] == symbol1.upper()].fillna(0)
    stock2 = df[df["SYMBOL"] == symbol2.upper()].fillna(0)

    return {
        "symbol1": {
            "symbol": symbol1.upper(),
            "avg_close": round(stock1["CLOSE"].mean(), 2),
            "avg_daily_return": round(stock1["DAILY_RETURN"].mean() * 100, 2),
            "volatility": round(stock1["VOLATILITY"].mean(), 4),
            "52w_high": stock1["52W_HIGH"].max(),
            "52w_low": stock1["52W_LOW"].min(),
        },
        "symbol2": {
            "symbol": symbol2.upper(),
            "avg_close": round(stock2["CLOSE"].mean(), 2),
            "avg_daily_return": round(stock2["DAILY_RETURN"].mean() * 100, 2),
            "volatility": round(stock2["VOLATILITY"].mean(), 4),
            "52w_high": stock2["52W_HIGH"].max(),
            "52w_low": stock2["52W_LOW"].min(),
        }
    }