"""Central Message Broker for the PoE Ecosystem."""

import asyncio
import json
from datetime import datetime
from typing import Set

import websockets
from loguru import logger
from pydantic import ValidationError

from shared_lib.models import PoeMessage

class MessageBroker:
    """Manages WebSocket connections and broadcasts messages."""

    def __init__(self, host: str = "localhost", port: int = 8888) -> None:
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        logger.info(f"Broker initialized on {host}:{port}")

    async def register(self, ws: websockets.WebSocketServerProtocol) -> None:
        """Register a new client connection."""
        self.clients.add(ws)
        logger.info(f"New client connected. Total clients: {len(self.clients)}")

    async def unregister(self, ws: websockets.WebSocketServerProtocol) -> None:
        """Unregister a client connection."""
        self.clients.remove(ws)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")

    async def broadcast(self, message_json: str) -> None:
        """Send a message to all connected clients."""
        if not self.clients:
            return

        logger.debug(f"Broadcasting message to {len(self.clients)} clients")
        # Prepare all send tasks to run concurrently
        send_tasks = [
            asyncio.create_task(client.send(message_json)) 
            for client in self.clients
        ]
        
        # Wait for all tasks to complete, ignoring failures of individual clients
        if send_tasks:
            await asyncio.wait(send_tasks)

    async def handler(self, ws: websockets.WebSocketServerProtocol) -> None:
        """Handle incoming WebSocket messages and lifecycle."""
        await self.register(ws)
        try:
            async for raw_message in ws:
                try:
                    # Validate against Pydantic model to ensure it follows the contract
                    data = json.loads(raw_message)
                    PoeMessage.model_validate(data)
                    
                    # If valid, broadcast to everyone
                    await self.broadcast(raw_message)
                    
                except ValidationError as e:
                    logger.warning(f"Invalid message format received: {e}")
                except json.JSONDecodeError:
                    logger.warning("Received non-JSON message")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(ws)

    async def start(self) -> None:
        """Start the WebSocket server."""
        logger.info(f"Starting Broker Server at ws://{self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    broker = MessageBroker()
    try:
        asyncio.run(broker.start())
    except KeyboardInterrupt:
        logger.info("Broker stopped by user")