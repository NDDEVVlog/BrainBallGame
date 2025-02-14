from Skill import Skill

import time
from Skill import Skill

class SkillHolder:
    
    def __init__(self, skills=None, maximum_mana=100, mana_regen_rate=5):
        """Initialize with an optional list of skills, maximum mana, and regen rate."""
        self.skills = {}  # Dictionary to store skills
        self.maximum_mana = maximum_mana  # Max mana cap
        self.current_mana = 0  # Start with full mana
        self.mana_regen_rate = mana_regen_rate  # Mana regeneration per second
        self.last_mana_update = time.time()  # Track last update time
        
        
        if skills:  # Add provided skills
            for skill in skills:
                self.skills[skill.name] = skill

    def add_skill(self, skill):
        """Add a skill to the skill set."""
        self.skills[skill.name] = skill

    def use_skill(self, skill_name: str):
        """Try to use a skill, deduct mana if successful."""
        self.regenerate_mana()  # Regenerate mana before using skill

        skill = self.skills.get(skill_name)
        if skill:
            if self.current_mana >= skill.mana_cost:
                print(f"Using skill: {skill.name}")
                skill.activate(None)
                self.current_mana -= skill.mana_cost  # Deduct mana
            else:
                print(f"Not enough mana to use {skill.name}.")
        else:
            print(f"Skill '{skill_name}' not found.")

    def regenerate_mana(self):
        """Regenerate mana over time."""
        current_time = time.time()
        elapsed_time = current_time - self.last_mana_update
        
        if elapsed_time > 0:
            regenerated_mana = self.mana_regen_rate * elapsed_time
            old_mana = self.current_mana  # Store previous mana for printing
            self.current_mana = min(self.current_mana + regenerated_mana, self.maximum_mana)
            self.last_mana_update = current_time  # Update last regen time1111
            
            #print(f"Mana Regenerated: {self.current_mana - old_mana:.2f} | Current Mana: {self.current_mana:.2f}/{self.maximum_mana}")


    def get_mana_info(self):
        """Return current and max mana for UI display."""
        return f"Mana: {int(self.current_mana)}/{self.maximum_mana}"
