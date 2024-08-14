from typing import List
from textual import on, events
from textual.app import App
from textual.widgets import Button, Input, Static, ListItem, ListView, Label
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import Reactive


class ChatHistoryListItem(Vertical):

    def __init__(self,
                 sender: str,
                 messageText: str,
                 classes: str | None = None):
        super().__init__()
        self.sender = sender
        self.messageText = messageText

    def compose(self):

        self.border_title = self.sender

        yield Label(self.messageText,classes="messageText")
            
