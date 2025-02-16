from SceneManager import SceneManager
from EEGGameUI import GameMenu
from Scene_Game import Scene_Game

if __name__ == "__main__":
    scene_manager = SceneManager()
    menu = GameMenu(scene_manager)
    game = Scene_Game(scene_manager)
    scene_manager.add_scene("Game", game)
    scene_manager.add_scene("Menu", menu)
    scene_manager.switch_scene("Menu")
    scene_manager.run()
