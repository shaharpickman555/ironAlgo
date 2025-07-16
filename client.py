import asyncio
import json
import random
import time
from datetime import datetime
import numpy as np
import calendar
from tqdm import tqdm
TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"]

async def send_request(ticker: str, timestamp: np.float64, callback):
    try:
        async def inner():
            reader, writer = await asyncio.open_connection('127.0.0.1', 5000)
            payload = json.dumps({"ticker": ticker, "timestamp": float(timestamp)})
            writer.write(payload.encode())
            await writer.drain()
            data = await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            return data

        data = await asyncio.wait_for(inner(), timeout=5.0)

        if data:
            response = json.loads(data.decode())
            await callback(ticker, timestamp, response["result"])
        else:
            await callback(ticker, timestamp, None)

    except asyncio.TimeoutError:
        await callback(ticker, timestamp, None)
    except Exception as e:
        await callback(ticker, timestamp, None)


async def callback_handler(ticker, timestamp, result):
    day = datetime.fromtimestamp(timestamp).date()
    if result is None:
        print(f"❌ No response for {ticker} on {day}")
    elif result == -1:
        print(f"⚠️  No data for {ticker} on {day}")
    else:
        print(f"✅ {ticker} on {day}: {result:.2f}")


async def run_client():
    while True:
        ticker = random.choice(TICKERS)
        year = 2025
        month = 7
        last_day = calendar.monthrange(year, month)[1]
        day = random.randint(1, last_day)
        date = datetime(year, month, day)
        timestamp = np.float64(time.mktime(date.timetuple()))
        print(f"\n📨 Sending request for {ticker} on {date.date()}")
        task = asyncio.create_task(send_request(ticker, timestamp, callback_handler))

        # Optional: show delay with progress bar
        # pbar = tqdm(total=10, desc="Waiting", leave=False)
        # for _ in range(10):
        #     await asyncio.sleep(0.1)
        #     pbar.update(1)
        # pbar.close()
        await task
        await asyncio.sleep(1)
