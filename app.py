from handlers.command_tunnel_handlers import CommandTunnelHandlers
from repositories.agent_repository import AgentRepository
from widgets.chat_screen import chat_screen
from textual.app import App

class AgentChat(App):

    CSS_PATH = "style.tcss"

    def compose(self):
        yield chat_screen

if __name__ == "__main__":
    CommandTunnelHandlers.apply_hadlers()
    AgentChat().run()