import pygame
import os
from constants import BALL_RADIUS, BALL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, RED
from SkillHolder import SkillHolder
from ListSkill import ChangeColor


class Ball:
    

    
    def __init__(self, x, y, image_path, fallback_color, controls):

        self.skillHolder = SkillHolder()
        self.image = None
        self.fallback_color = fallback_color
        self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.velocity = [0, 0]
        self.controls = controls  # Dict containing key mappings

        self.skillHolder.add_skill(ChangeColor(self))
        
        # Check if the image path is valid
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

    def move(self, keys):
        if keys[self.controls['left']]:
            self.velocity[0] = -BALL_SPEED
        elif keys[self.controls['right']]:
            self.velocity[0] = BALL_SPEED
        else:
            self.velocity[0] = 0
        
        # if keys[self.controls['up']]:
        #     self.velocity[1] = -BALL_SPEED
        # elif keys[self.controls['down']]:
        #     self.velocity[1] = BALL_SPEED
        # else:
        #     self.velocity[1] = 0

        self.rect.move_ip(self.velocity)
        
    def move_based_on_focus(self, meditation_value, attention_value,reverse_movement:bool):
        if meditation_value > attention_value:
            direction = -1 if reverse_movement else 1
            self.velocity[0] = BALL_SPEED * direction
        else:
            self.velocity[0] = 0  # Stop moving if attention is higher

        self.rect.move_ip(self.velocity)
        

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(screen, self.fallback_color, self.rect.center, BALL_RADIUS)

    def check_collision(self, other_ball):
        if self.rect.colliderect(other_ball.rect):
            # Swap velocities to make them bounce off each other
            self.velocity, other_ball.velocity = other_ball.velocity, self.velocity
            # Move them slightly apart to avoid sticking
            self.rect.move_ip(self.velocity)
            other_ball.rect.move_ip(other_ball.velocity)

    def GetSkillHolder(self):
        return self.skillHolder
    
    def use_skill(self, keys):
        """Use the skill based on the pressed key dynamically."""
        skill_names = list(self.skillHolder.skills.keys())  # Get available skills dynamically

        for i in range(1, 4):  # Skill_1, Skill_2, Skill_3
            skill_key = self.controls.get(f'Skill_{i}')  # Get key assigned to the skill
            
            # Corrected the way to check key states
            if skill_key and keys[skill_key] and (i - 1) < len(skill_names):
                self.mana = self.skillHolder.use_skill(skill_names[i - 1])  # Use skill
