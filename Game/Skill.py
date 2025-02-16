from GameEnum import SkillType
from abc import ABC, abstractmethod
import pygame
import time
import os

# Define a unique event for skill cooldown completion
SKILL_COOLDOWN_EVENT = pygame.USEREVENT + 1

class Skill:
    def __init__(self, name: str, description: str, cooldown: float, mana_cost: float, skill_type: SkillType, image_path: str):
        self.name = name
        self.description = description
        self.cooldown = cooldown  # Cooldown time in seconds
        self.mana_cost = mana_cost  # Mana required to use
        self.skill_type = skill_type  # Enum (e.g., ATTACK, DEFENSE)
        self.on_cooldown = False  # Track cooldown state
        self.cooldown_end_time = 0  # Track when cooldown ends
        
        # Ensure image path is valid
        if os.path.isfile(image_path):
            self.image_path = image_path
        else:
            print(f"⚠️ Warning: Image file not found ({image_path}), using default '?' image.")
            self.image_path = "C:/Users/Admin/BrainBallGame/Resources/TestAvartar/pop_cat.png"

    def can_use(self, current_mana):
        """Check if the skill can be used (must have enough mana & cooldown must be over)."""
        current_time = time.time()
        
        if self.on_cooldown:
            remaining_time = round(self.cooldown_end_time - current_time, 2)
            if remaining_time > 0:
                print(f"{self.name} is on cooldown. {remaining_time}s left.")
                return False
            else:
                self.on_cooldown = False  # Reset cooldown state if time is up

        if current_mana < self.mana_cost:
            print(f"Not enough mana to use {self.name}. Requires {self.mana_cost} MP.")
            return False
        return True

    def use(self, current_mana):
        """Use the skill if possible."""
        if self.can_use(current_mana):
            self.on_cooldown = True
            self.cooldown_end_time = time.time() + self.cooldown  # Set when cooldown ends
            print(f"{self.name} activated! {self.description}")
            return self.mana_cost  # Return mana consumed
        return 0  # No mana consumed if skill wasn't used

    def get_remaining_cooldown(self):
        """Returns remaining cooldown time or 0 if skill is ready."""
        if self.on_cooldown:
            remaining_time = round(self.cooldown_end_time - time.time(), 2)
            return max(0, remaining_time)  # Ensure it never goes negative
        return 0

    def draw_cooldown(self, screen, x, y, font):
        """Display cooldown time on screen (for UI)."""
        remaining_time = self.get_remaining_cooldown()
        if remaining_time > 0:
            cooldown_text = font.render(f"{self.name}: {remaining_time}s", True, (255, 0, 0))
            screen.blit(cooldown_text, (x, y))

    
    
    @abstractmethod
    def CoolDownComplete(self,target):
        pass

    @abstractmethod
    def activate(self, target):
        """Abstract method that must be implemented in subclasses."""
        pass  # This must be overridden in child classes
        