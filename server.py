import asyncio
import json
import numpy as np
import yfinance as yf
import datetime
import time
UNREACHABLE_INTERVAL = 5 * 60 #5 mins
start_time = time.time()

def get_data(ticker: str, timestamp: np.float64) -> np.float32:
    try:
        dt = datetime.datetime.fromtimestamp(timestamp).date()
        df = yf.download(ticker, start=dt.isoformat(), end=(dt + datetime.timedelta(days=1)).isoformat(),
                         interval='1d',progress=False,auto_adjust=True)
        if not df.empty:
            return np.float32(df['Close'].iloc[0])
        else:
            return np.float32(-1)
    except Exception as e:
        print("Error fetching data:", e)
        return np.float32(-1)


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    elapsed = time.time() - start_time
    if int(elapsed) % UNREACHABLE_INTERVAL == 0:
        print("🚫 Simulating server hang...")
        await asyncio.sleep(999)
    try:
        data = await reader.read(1024)
        if not data:
            return

        request = json.loads(data.decode())
        ticker = request["ticker"]
        timestamp = np.float64(request["timestamp"])

        result = get_data(ticker, timestamp)
        response = json.dumps({"result": float(result)})
        writer.write(response.encode())
        await writer.drain()
    except Exception as e:
        print("Error handling client:", e)
    finally:
        writer.close()
        await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5000)
    print("📡 Async Server running on port 5000")

    async with server:
        await server.serve_forever()
