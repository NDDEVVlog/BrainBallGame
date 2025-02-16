import threading
from Skill import Skill
from SkillHolder import SkillHolder
from GameEnum import SkillType
import pygame

class ChangeColor(Skill):
    def __init__(self,skillHolder ,player):
        super().__init__(
            name="ChangeColor",
            description="Change the ball color to Green for 5s.",
            cooldown=5,
            mana_cost=15,
            skill_type=SkillType.ACTIVE,
            image_path="heal.png"
        )
        self.skillHolder = skillHolder
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


class Freeze(Skill):
    def __init__(self,skillHolder,player):
        super().__init__(
            name="Freeze",
            description="Prevents movement and pushback for 3s.",
            cooldown=10,
            mana_cost=20,
            skill_type=SkillType.ACTIVE,
            image_path="freeze.png"
        )
        self.skillHolder = skillHolder
        self.player = player
        self.is_active = False

    def activate(self, target):
        if self.is_active:
            print("Freeze is already active.")
            return
        
        self.previousColor = self.player.fallback_color
        self.player.fallback_color = (102, 241, 245)
        self.is_active = True
        self.player.isFrozen = True  # Prevent movement and pushback


        threading.Timer(10, self.revert_freeze).start()

    def revert_freeze(self):
        self.player.isFrozen = False
        print("Freeze effect ended.")
        self.player.fallback_color =  self.previousColor
        self.is_active = False


class Dash(Skill):
    def __init__(self,skillHolder ,player):
        super().__init__(
            name="Dash",
            description="Quickly moves the player forward.",
            cooldown=7,
            mana_cost=10,
            skill_type=SkillType.ACTIVE,
            image_path="dash.png"
        )
        self.skillHolder = skillHolder
        self.player = player

    def activate(self, target):
        if self.player.is_frozen:
            print("Cannot dash while frozen!")
            return

        dash_speed = 10  # Set a higher speed for a quick dash
        self.player.x += self.player.direction * dash_speed
        print(f"{target} dashed forward!")


class ManaBoost(Skill):
    def __init__(self,skillHolder ,player):
        super().__init__(
            name="Mana Boost",
            description="Increases mana regeneration rate.",
            cooldown=0,  # Passive skill, always active
            mana_cost=0,
            skill_type=SkillType.PASSIVE,
            image_path="mana_boost.png"
        )
        self.skillHolder = skillHolder
        self.player = player
        self.mana_regen_bonus = 2  # Increase regen rate

    def apply_effect(self):
        """Passively increases mana regeneration."""
        self.skillHolder.mana_regen_rate += self.mana_regen_bonus
        print(f"Mana regeneration increased by {self.mana_regen_bonus}!")


class Shield(Skill):
    def __init__(self,skillHolder, player):
        super().__init__(
            name="Shield",
            description="Reduces damage taken for 5 seconds.",
            cooldown=12,
            mana_cost=25,
            skill_type=SkillType.ACTIVE,
            image_path="shield.png"
        )
        self.skillHolder = skillHolder
        self.player = player
        self.is_active = False

    def activate(self, target):
        if self.is_active:
            print("Shield is already active.")
            return

        self.is_active = True
        self.player.damage_reduction = 0.5  # Reduce damage by 50%
        print(f"{target} activated Shield!")

        threading.Timer(5, self.revert_shield).start()

    def revert_shield(self):
        self.player.damage_reduction = 1.0  # Reset damage reduction
        print("Shield effect ended.")
        self.is_active = False