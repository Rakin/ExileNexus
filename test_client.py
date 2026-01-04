import asyncio
import websockets
import sys

async def listen():
    url = "ws://localhost:8888"
    print(f"[*] Attempting to connect to {url}...")
    try:
        async with websockets.connect(url) as ws:
            print(f"[+] Connected successfully to Broker!")
            print("[*] Waiting for messages (Press Ctrl+C to stop)...")
            async for message in ws:
                print(f"[MESSAGE RECEIVED]: {message}")
    except ConnectionRefusedError:
        print("[-] Error: Connection refused. Is the Broker (hub.py) running?")
    except Exception as e:
        print(f"[-] An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        print("\n[!] Client stopped by user.")
        sys.exit(0)