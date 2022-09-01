'''Main Menu View'''
import arcade
import arcade.gui

from views.view import View
from views.gameView import GameView
from views.gameOverView import GameOverView
from views.winnerView import WinnerView

class MainMenuView(View):
    def __init__(self):
        super().__init__()
        
        #vertikalni BoxGroup za botune
        self.v_box = None
        
    def setup(self):
        super().setup()
        self.ui_manager = arcade.gui.UIManager()
        
        self.setup_botune()
        
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        
    def setup_botune(self):
        self.v_box = arcade.gui.UIBoxLayout()
        
        play_botun = arcade.gui.UIFlatButton(text="Start Game", width=200)
        @play_botun.event("on_click")
        def on_click_play(event):
            if "game" not in self.window.views:
                self.window.views["game"] = GameView()
                self.window.views["game_over"] = GameOverView()
                self.window.views["winner"] = WinnerView()
            self.window.show_view(self.window.views["game"])
        self.v_box.add(play_botun.with_space_around(bottom=20))
        
        quit_botun = arcade.gui.UIFlatButton(text="Quit", width=200)
        @quit_botun.event("on_click")
        def on_click_quit(event):
            arcade.exit()
        self.v_box.add(quit_botun)
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text(
            "Arcade platformer",
            self.window.width / 2,
            self.window.height - 125,
            arcade.color.ALLOY_ORANGE,
            font_size=44,
            anchor_x="center",
            anchor_y="center"
        )
        
        self.ui_manager.draw()