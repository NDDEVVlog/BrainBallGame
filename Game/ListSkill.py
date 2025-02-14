from Skill import Skill
from GameEnum import SkillType

class ChangeColor(Skill):
    def __init__(self,player):
        
        super().__init__(
            name="ChangeColor",
            description="Change the ball color to Green.",
            cooldown=5,
            mana_cost=15,
            skill_type=SkillType.ACTIVE,
            image_path="heal.png"
        )
        self.player = player

    def activate(self, target):
        """Change the color of the target (ball) to green."""
        self.player.fallback_color = (0, 255, 0)  # Green color
        print(f"{target} changed color to GREEN!")