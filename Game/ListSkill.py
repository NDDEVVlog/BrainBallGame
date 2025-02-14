import threading
from Skill import Skill
from GameEnum import SkillType
import pygame

class ChangeColor(Skill):
    def __init__(self, player):
        super().__init__(
            name="ChangeColor",
            description="Change the ball color to Green for 5s.",
            cooldown=5,
            mana_cost=15,
            skill_type=SkillType.ACTIVE,
            image_path="heal.png"
        )
        self.player = player
        self.is_active = False  # Prevents multiple activations

    def activate(self, target):
        """Change the color of the target (ball) to green for 5 seconds."""
        if self.is_active:
            print("Skill is already active. Wait for it to revert.")
            return  # Prevents reactivation

        self.is_active = True
        self.previousColor = self.player.fallback_color
        print(f"previousColor color: {self.previousColor}")

        self.player.fallback_color = (0, 255, 0)  # Green color
        print(f"{target} changed color to GREEN!")

        # Start a thread timer to revert the color after 5 seconds
        threading.Timer(5, self.revert_color).start()

    def revert_color(self):
        """Reverts the player's color to original."""
        self.player.fallback_color = self.previousColor  # Restore original color
        print(f"Reverted color back to original: {self.player.fallback_color}")

        # Reset state to allow future activation
        self.is_active = False
