import asyncio
import websockets

async def handle_websocket(websocket, path):
    print(f"WebSocket connection established from {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received message: {message}")

            # Handle the message here as needed
            # For example, parse JSON if message is JSON formatted

            # Echo back the message for testing
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print(f"WebSocket connection closed with {websocket.remote_address}")

async def main():
    async with websockets.serve(handle_websocket, '127.0.0.1', 65432):
        print("WebSocket server started.")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
