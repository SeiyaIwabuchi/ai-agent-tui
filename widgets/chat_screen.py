import asyncio
from enum import IntEnum, auto
import traceback

from textual import on
from textual.widgets import Button, Input, Static, Select
from textual.containers import Horizontal, Vertical

from models.chat_history_model import ChatHistoryModel
from repositories.agent_repository import AgentRepository
from repositories.internal_message_queue import internal_message_queue
from widgets.chat_history_list_view import ChatHistoryListView

class Mode(IntEnum):
    Agent = auto()
    SimpleChat = auto()

class ChatScreen(Vertical):

    async def queue_loop(self):
        while True:
            if not internal_message_queue.empty():
                self.chat_history_list_view.append(internal_message_queue.get())
            await asyncio.sleep(1)

    def compose(self):

        self.chat_history_list_view = ChatHistoryListView(id="historyListView")
        self.input = Input(placeholder="プロンプトを入力...", id="promptFormInput")
        self.mode_select = Select(((Mode.Agent.name, Mode.Agent), (Mode.SimpleChat.name, Mode.SimpleChat),), allow_blank=False, value=Mode.Agent, id="modeSelect")

        asyncio.create_task(self.queue_loop())

        # コンテナにウィジェットを追加
        yield Vertical(
            Static("履歴", classes="notes"),
            self.chat_history_list_view,
            id="chatHistory"
        )
        yield Horizontal(
            self.mode_select,
            self.input,
            Button("送信", id="promptFormAddButton"),
            id="promptForm"
        )
    
    @on(Button.Pressed, "#promptFormAddButton")
    async def on_send_presses(self, event: Button.Pressed):
        prompt = self.input.value
        self.input.value = ""
        self.chat_history_list_view.append(ChatHistoryModel("あなた", prompt))

        if self.mode_select.value == Mode.Agent:
            try:
                response = await AgentRepository.sendMessage(prompt)
                client_id = response["client_id"]
                websocketapp = AgentRepository.startCommandTunnel(client_id)
                agent_response = await AgentRepository.wait_for_agent_task(client_id)
                self.chat_history_list_view.append(ChatHistoryModel("エージェント", agent_response["answer"]))
            except:
                self.chat_history_list_view.append(ChatHistoryModel("システムエラー", traceback.format_exc()))
            finally:
                websocketapp.close()
        else:
            try:
                response = await AgentRepository.simple_chat(prompt)
                self.chat_history_list_view.append(ChatHistoryModel("エージェント", response["answer"]))
            except:
                self.chat_history_list_view.append(ChatHistoryModel("システムエラー", traceback.format_exc()))


chat_screen = ChatScreen()