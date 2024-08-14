from typing import List
from textual import on, events
from textual.app import App
from textual.widgets import Button, Input, Static, ListItem, ListView, Label
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual.reactive import Reactive

from models.chat_history_model import ChatHistoryModel
from widgets.chat_history_list_item import ChatHistoryListItem

class ChatHistoryListView(VerticalScroll):

    chatHistory: List[ChatHistoryModel] = [
        ChatHistoryModel("あなた", "こんちにあ！"),
        ChatHistoryModel("エージェント", "こんにちわ。今日はいい天気ですね。")
    ]


    def compose(self):
        for history in self.chatHistory:
            yield ChatHistoryListItem(history.sender, history.message)


    def append(self, chatHistory: ChatHistoryModel):
        self.chatHistory.append(chatHistory)
        self.mount_all(self.compose())
        self.scroll_end(animate=False)
        