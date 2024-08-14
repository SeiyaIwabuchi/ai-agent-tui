import asyncio
from repositories.agent_repository import AgentRepository
from websocket import WebSocket
import subprocess
import time

class CommandTunnelHandlers:

    @staticmethod
    def on_message(ws: WebSocket, message):
        try:
            result = subprocess.run(message, shell=True, capture_output=True, text=True, check=True)
            print(f"{result.returncode=}")
            print(f"{result.stdout=}")
            print(f"{result.stderr=}")
            ws.send(result.stdout + "\n" + result.stderr)
        except subprocess.CalledProcessError as result:
            print(f"{result.returncode=}")
            print(f"{result.stdout=}")
            print(f"{result.stderr=}")
            ws.send(result.stdout + "\n" + result.stderr)

    retrring = False

    @staticmethod
    def on_close(ws: WebSocket, close_status_code, close_msg):
            if not CommandTunnelHandlers.retrring:
                CommandTunnelHandlers.retrring = True
                time.sleep(3)
                AgentRepository.startCommandTunnel()
                CommandTunnelHandlers.retrring = False

    @staticmethod
    def on_open(ws: WebSocket):
         CommandTunnelHandlers.retrring = False

    @classmethod
    def apply_hadlers(self):
        AgentRepository.on_message = CommandTunnelHandlers.on_message
        AgentRepository.on_close = CommandTunnelHandlers.on_close
        AgentRepository.on_open = CommandTunnelHandlers.on_open