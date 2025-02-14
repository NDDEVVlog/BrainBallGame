from GameEnum import SkillType
from abc import ABC, abstractmethod
import time
import os


class Skill:
    def __init__(self, name: str, description: str, cooldown: float, mana_cost: float, skill_type: SkillType, image_path: str):
        self.name = name
        self.description = description
        self.cooldown = cooldown  # Cooldown time in seconds
        self.mana_cost = mana_cost  # Mana required to use
        self.skill_type = skill_type  # Enum (e.g., ATTACK, DEFENSE)
        
        # Ensure image path is valid
        if os.path.isfile(image_path):
            self.image_path = image_path
        else:
            print(f"⚠️ Warning: Image file not found ({image_path}), using default '?' image.")
            self.image_path = "C:/Users/Admin/BrainBallGame/Resources/TestAvartar/pop_cat.png"  # Provide a default '?' image

        
        self.image_path = image_path  # Store the valid image path
        self.last_used = 0  # Timestamp for cooldown tracking

    def can_use(self, current_mana):
        """Check if skill can be used (enough mana + not on cooldown)."""
        if time.time() - self.last_used < self.cooldown:
            remaining_time = round(self.cooldown - (time.time() - self.last_used), 2)
            print(f"{self.name} is on cooldown. {remaining_time}s left.")
            return False
        if current_mana < self.mana_cost:
            print(f"Not enough mana to use {self.name}. Requires {self.mana_cost} MP.")
            return False
        return True

    def use(self, current_mana):
        """Activate the skill if possible."""
        if self.can_use(current_mana):
            self.last_used = time.time()
            print(f"{self.name} activated! {self.description}")
            
            return self.mana_cost  # Return mana consumed
        return 0  # No mana consumed if skill wasn't used
    
    @abstractmethod
    def activate(self, target ):
        """Abstract method that must be implemented in subclasses."""
        pass  # This must be overridden in child classes