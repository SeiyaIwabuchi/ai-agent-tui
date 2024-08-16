import asyncio
from typing import Any, Callable
from websocket import WebSocketApp, WebSocket
import httpx

class AgentRepository:

    host = "172.18.0.3:8000"

    @classmethod
    async def sendMessage(self, message: str) -> dict[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://{self.host}/agent", json={ "message" : message })
            response.raise_for_status()
            return response.json()
    
    @classmethod
    async def wait_for_agent_task(self, client_id: str):
        async with httpx.AsyncClient(timeout=httpx.Timeout(3600)) as client:
            response = await client.get(f"http://{self.host}/wait_for_agent_task/{client_id}")
            response.raise_for_status()
            return response.json()
        
    @classmethod
    async def simple_chat(self, message: str):
        async with httpx.AsyncClient(timeout=httpx.Timeout(3600)) as client:
            response = await client.post(f"http://{self.host}/chat", json={ "message" : message })
            response.raise_for_status()
            return response.json()

    # websocketの設定

    on_message: Callable[[WebSocket, Any], None] = lambda ws, x: None
    on_error: Callable[[WebSocket, Any], None] = lambda ws, x: None
    on_close: Callable[[WebSocket, Any, Any], None] = lambda ws, x, y: None
    on_open: Callable[[WebSocket], None] = lambda ws: None

    commandTunnel: WebSocketApp = None

    commandTunnelUrl = f"ws://{host}/ws/"
    commandTunnelUrl += "{client_id}"

    @staticmethod
    def _common(ws: WebSocket):
        pass

    @staticmethod
    def _on_message(ws: WebSocket, message):
        AgentRepository._common(ws)
        print("Received:", message)
        AgentRepository.on_message(ws, message)

    @staticmethod
    def _on_error(ws: WebSocket, error):
        AgentRepository._common(ws)
        print("Error:", error)
        AgentRepository.on_error(ws, error)

    @staticmethod
    def _on_close(ws: WebSocket, close_status_code, close_msg):
        AgentRepository._common(ws)
        print("Closed")
        AgentRepository.on_close(ws, close_status_code, close_msg)

    @staticmethod
    def _on_open(ws: WebSocket):
        AgentRepository._common(ws)
        print("Opened")
        AgentRepository.on_open(ws)

    @classmethod
    def startCommandTunnel(self, client_id: str):
        self.commandTunnel = WebSocketApp(
            self.commandTunnelUrl.format(client_id = client_id),
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

        asyncio.new_event_loop().run_in_executor(
            None,
            self.commandTunnel.run_forever,
            ()
        )

        return self.commandTunnel
