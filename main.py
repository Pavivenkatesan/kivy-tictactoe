#!/usr/bin/env python3

import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import WipeTransition

from lib.view.mainmenuview import MainMenuView
from lib.view.singleplayerview import SinglePlayerView
from lib.view.botplayerview import BotPlayerView


class TicTacToeApp(App):

	title = "Tic-Tac-Toe"
	icon = "assets/icon.ico"


	def init_screen(self):
		screenManager = ScreenManager(transition = WipeTransition())
		screenManager.add_widget(MainMenuView(name = "mainmenu"))
		screenManager.add_widget(SinglePlayerView(name = "singleplayer-gameplay"))
		screenManager.add_widget(BotPlayerView(name="botplayer-gameplay"))
		return screenManager


	def init_config(self):
		Config.set("graphics", "fullscreen", 0)
		Config.set("graphics", "resizable", 0)
		Config.set("graphics", "height", 600)
		Config.set("graphics", "width", 600)
		Config.set("kivy", "exit_on_escape", 0)
		Config.set("input", "mouse", "mouse,multitouch_on_demand")
		Config.write()


	def build(self):
		self.init_config()
		return self.init_screen()


if __name__ == "__main__":
	TicTacToeApp().run()
