import traceback

from typing import List
from textual import on, events
from textual.app import App
from textual.widgets import Button, Input, Static, ListItem, ListView, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import Reactive

from models.chat_history_model import ChatHistoryModel
from repositories.agent_repository import AgentRepository
from widgets.chat_history_list_view import ChatHistoryListView


class ChatScreen(Vertical):

    def compose(self):

        self.chat_history_list_view = ChatHistoryListView(id="historyListView")
        self.input = Input(placeholder="プロンプトを入力...", id="promptFormInput")

        # コンテナにウィジェットを追加
        yield Vertical(
            Static("履歴", classes="notes"),
            self.chat_history_list_view,
            id="chatHistory"
        )
        yield Horizontal(
            self.input,
            Button("送信", id="promptFormAddButton"),
            id="promptForm"
        )
    
    @on(Button.Pressed, "#promptFormAddButton")
    async def on_send_presses(self, event: Button.Pressed):
        prompt = self.input.value
        self.input.value = ""
        self.chat_history_list_view.append(ChatHistoryModel("あなた", prompt))

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


chat_screen = ChatScreen()