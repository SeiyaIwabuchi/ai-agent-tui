import asyncio
from enum import IntEnum, auto
import traceback

from textual import on
from textual.widgets import Button, Input, Static, Select
from textual.containers import Horizontal, Vertical
from textual.events import Key, InputEvent
from textual.reactive import Reactive

from models.chat_history_model import ChatHistoryModel
from repositories.agent_repository import AgentRepository
from repositories.internal_message_queue import internal_message_queue
from widgets.chat_history_list_view import ChatHistoryListView

class Mode(IntEnum):
    Agent = auto()
    SimpleChat = auto()

class ChatScreen(Vertical):

    input_history: Reactive[list[str]] = Reactive([])
    current_index: Reactive[int] = Reactive(-1)

    async def queue_loop(self):
        while True:
            if not internal_message_queue.empty():
                self.chat_history_list_view.append(internal_message_queue.get())
            await asyncio.sleep(1)

    def compose(self):

        self.chat_history_list_view = ChatHistoryListView(id="historyListView")
        self.input = Input(placeholder="プロンプトを入力...", id="promptFormInput")
        self.mode_select = Select(((Mode.Agent.name, Mode.Agent), (Mode.SimpleChat.name, Mode.SimpleChat),), allow_blank=False, value=Mode.Agent, id="modeSelect")
        self.add_button = Button("送信", id="promptFormAddButton")

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
            self.add_button,
            id="promptForm"
        )
    
    @on(Button.Pressed, "#promptFormAddButton")
    async def on_send_presses(self, event: Button.Pressed):
        prompt = self.input.value
        self.input.value = ""
        self.chat_history_list_view.append(ChatHistoryModel("あなた", prompt))

        if self.mode_select.value == Mode.Agent:
            try:
                if not await AgentRepository.is_alive_thread():
                    AgentRepository.client_id = (await AgentRepository.start_thread())["client_id"]
                websocketapp = AgentRepository.startCommandTunnel()
                agent_response = await AgentRepository.wait_for_agent_task(prompt)
                self.chat_history_list_view.append(ChatHistoryModel("エージェント", agent_response["answer"]))
            except:
                self.chat_history_list_view.append(ChatHistoryModel("システムエラー", traceback.format_exc()))
                traceback.print_exc()
            finally:
                websocketapp.close()
        else:
            try:
                response = await AgentRepository.simple_chat(prompt)
                self.chat_history_list_view.append(ChatHistoryModel("エージェント", response["answer"]))
            except:
                self.chat_history_list_view.append(ChatHistoryModel("システムエラー", traceback.format_exc()))


    async def handle_key(self, event: Key) -> bool:
        if event.key == "enter":
            text = self.input.value
            if text:
                self.input_history.append(text)
                self.current_index = len(self.input_history)
                self.add_button.action_press()

        elif event.key == "up":
            if self.input_history and self.current_index > 0:
                self.current_index -= 1
                self.input.value = self.input_history[self.current_index]

        elif event.key == "down":
            if self.input_history and self.current_index < len(self.input_history) - 1:
                self.current_index += 1
                self.input.value = self.input_history[self.current_index]
            else:
                self.current_index = len(self.input_history)
                self.input.value = ""
        return await super().handle_key(event)

    async def on_key(self, event: Key):
        if self.input.has_focus:
            await self.handle_key(event)

chat_screen = ChatScreen()