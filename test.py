import numpy as np
import yfinance as yf
import time
import datetime

def get_data(ticker: str, timestamp: np.float64) -> np.float32:
    dt = datetime.datetime.fromtimestamp(timestamp).date()
    df = yf.download(ticker, start=dt.isoformat(), end=(dt + datetime.timedelta(days=1)).isoformat(), interval='1d',
                     progress=False)
    if not df.empty:
        return np.float32(df['Close'].iloc[0])
    else:
        return np.float32(-1)

def main():
    ticker_symbol = "AAPL"
    ts = np.float64(time.mktime(time.strptime("2025-07-15", "%Y-%m-%d")))
    result = get_data(ticker_symbol, ts)
    print(f"Price on that date: {result}")

if __name__ == "__main__":
    main()
