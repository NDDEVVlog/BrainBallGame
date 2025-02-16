import pygame

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.running = True

    def add_scene(self, name, scene):
        """Add a scene to the manager."""
        self.scenes[name] = scene
        print(f"Scene '{name}' added successfully.")

    def switch_scene(self, name):
        """Switch to another scene if it exists."""
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            print(f"Switched to scene '{name}'.")
        else:
            print(f"Scene '{name}' not found!")

    def run(self):
        """Run the current scene's loop."""
        while self.current_scene and self.running:
            self.current_scene.run()
    
    def get_scene(self, name):
        """Retrieve a scene by name."""
        return self.scenes[name]
    
    def ForceExit(self):
        self.running = False
