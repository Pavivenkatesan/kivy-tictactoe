from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from lib.view.singleplayerview import SinglePlayerView
from lib.view.botplayerview import BotPlayerView
import time

class MainMenuView(Screen):
    soundClick = SoundLoader.load("assets/menu_selection_click.ogg")
    _isOver = False

    def btnHumanPlayer_release(self):
        humanGame = SinglePlayerView()
        humanGame.restart_game()
        self.manager.current = "singleplayer-gameplay"

    def btnBotPlayer_release(self):
        botGame = BotPlayerView()
        botGame.restart_game()
        self.manager.current = "botplayer-gameplay"

    def btnExit_release(self):
        App.get_running_app().stop()
