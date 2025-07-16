import asyncio
from multiprocessing import Process

def start_server():
    from server import run_server
    asyncio.run(run_server())

def start_client():
    from client import run_client
    asyncio.run(run_client())

def run_builder():
    server = Process(target=start_server)
    server.start()
    client = Process(target=start_client)
    client.start()
    server.join()
    client.join()

if __name__ == "__main__":
    run_builder()
