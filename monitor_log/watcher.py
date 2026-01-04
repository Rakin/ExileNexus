import asyncio
import os
from pathlib import Path
import websockets
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from shared_lib.models import EventType, MessageHeader, PoeMessage

class LogHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_modified(self, event):
        if not event.is_directory and Path(event.src_path) == self.watcher.log_path:
            # Agenda a leitura no loop principal do asyncio
            self.watcher.loop.call_soon_threadsafe(
                lambda: asyncio.create_task(self.watcher.read_new_lines())
            )

class LogWatcher:
    def __init__(self, log_path: Path, broker_url: str):
        self.log_path = log_path
        self.broker_url = broker_url
        self.loop = asyncio.get_event_loop()
        self.last_position = os.path.getsize(log_path) if log_path.exists() else 0
        self.websocket = None
        self.observer = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.broker_url)
            logger.info("Connected to Broker")
        except Exception as e:
            logger.error(f"Broker connection failed: {e}")

    async def read_new_lines(self):
        try:
            # Shared read mode
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self.last_position)
                lines = f.readlines()
                self.last_position = f.tell()
                
                for line in lines:
                    if " : You have entered " in line:
                        await self.send_to_broker(line.strip())
        except Exception as e:
            logger.error(f"Error reading file: {e}")

    async def send_to_broker(self, line: str):
        area_name = line.split(" : You have entered ")[1].rstrip(".")
        logger.success(f"Watchdog Detected: {area_name}")
        
        message = PoeMessage(
            header=MessageHeader(source="monitor_log", event_type=EventType.AREA_ENTERED),
            payload={"area_name": area_name}
        )
        
        if self.websocket and self.websocket.state.name == "OPEN":
            await self.websocket.send(message.model_dump_json())

    async def start(self):
        await self.connect()
        
        # Configura o Watchdog
        event_handler = LogHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.log_path.parent), recursive=False)
        self.observer.start()
        
        logger.info(f"Watchdog monitoring: {self.log_path}")
        
        try:
            while True:
                await asyncio.sleep(1) # Mantém o loop vivo
        except asyncio.CancelledError:
            self.observer.stop()
        self.observer.join()

async def main():
    path = Path("test_client.txt")
    if not path.exists(): path.touch()
    
    watcher = LogWatcher(path, "ws://localhost:8888")
    await watcher.start()

if __name__ == "__main__":
    asyncio.run(main())