import arcade

from konstante import VISINA_PROZORA, SIRINA_PROZORA, NASLOV_PROZORA
from views.mainMenuView import MainMenuView
class GameProzor(arcade.Window):
    def __init__(self):
        super().__init__(SIRINA_PROZORA, VISINA_PROZORA, NASLOV_PROZORA, resizable = False)
        
        self.views = {}
        self.views["main_menu"] = MainMenuView()
        
def main() -> None:
    window = GameProzor()
    window.show_view(window.views["main_menu"])
    arcade.run()
    
if __name__ == "__main__":
    main()