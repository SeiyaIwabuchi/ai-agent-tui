from textual.widgets import Markdown
from textual.containers import Vertical


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

        yield Markdown(self.messageText,classes="messageText")
            
