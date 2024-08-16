import asyncio
import json
from models.chat_history_model import ChatHistoryModel
from repositories.internal_message_queue import internal_message_queue
from repositories.agent_repository import AgentRepository
from websocket import WebSocket
import subprocess
import time
import traceback

from widgets.chat_screen import chat_screen

class CommandTunnelHandlers:

    @staticmethod
    def on_message(ws: WebSocket, message):
        try:
            command = json.loads(message)["command"]
            internal_message_queue.put(ChatHistoryModel("Debug Message", f"Execute command : {command}"))
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"{result.returncode=}")
            print(f"{result.stdout=}")
            print(f"{result.stderr=}")
            exec_result = {
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            internal_message_queue.put(ChatHistoryModel("Debug Message", f"Retuen message to server\n----------\n{exec_result}"))
            ws.send(json.dumps(exec_result))
        except subprocess.CalledProcessError as result:
            print(f"{result.returncode=}")
            print(f"{result.stdout=}")
            print(f"{result.stderr=}")
            exec_result = {
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            internal_message_queue.put(ChatHistoryModel("Debug Message", f"Retuen message to server \n----------\n{exec_result}"))
            ws.send(json.dumps(exec_result))
        except:
            trace = traceback.format_exc()
            ws.close()
            breakpoint()

    retrring = False

    @staticmethod
    def on_close(ws: WebSocket, close_status_code, close_msg):
        pass
            # if not CommandTunnelHandlers.retrring:
            #     CommandTunnelHandlers.retrring = True
            #     time.sleep(3)
            #     AgentRepository.startCommandTunnel()
            #     CommandTunnelHandlers.retrring = False

    @staticmethod
    def on_open(ws: WebSocket):
         CommandTunnelHandlers.retrring = False

    @classmethod
    def apply_hadlers(self):
        AgentRepository.on_message = CommandTunnelHandlers.on_message
        AgentRepository.on_close = CommandTunnelHandlers.on_close
        AgentRepository.on_open = CommandTunnelHandlers.on_open