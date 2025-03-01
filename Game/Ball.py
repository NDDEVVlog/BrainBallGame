import pygame
import os
from constants import BALL_RADIUS, BALL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, RED
from SkillHolder import SkillHolder
from SkillList import ChangeColor,Freeze


class Ball:
    

    
    def __init__(self, x, y, image_path, fallback_color, controls):

        self.skillHolder = SkillHolder()
        self.isFrozen = False
        
        self.image = None
        self.fallback_color = fallback_color
        self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.velocity = [0, 0]
        self.controls = controls  # Dict containing key mappings

        self.skillHolder.add_skill(ChangeColor(self.skillHolder,self))
        self.skillHolder.add_skill(Freeze(self.skillHolder,self))
        
        # Check if the image path is valid
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

    def move(self, keys):
        if self.isFrozen:
            return  # Prevent movement when frozen

        if keys[self.controls['left']]:
            self.velocity[0] = -BALL_SPEED
        elif keys[self.controls['right']]:
            self.velocity[0] = BALL_SPEED
        else:
            self.velocity[0] = 0

        self.rect.move_ip(self.velocity)

        # Clamp the position to keep the ball inside the screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def move_based_on_focus(self, meditation_value, attention_value, reverse_movement: bool):
        if self.isFrozen:
            print("is being Frozen")
            return  # Prevent movement when frozen

        if meditation_value > attention_value:
            direction = -1 if reverse_movement else 1
            self.velocity[0] = BALL_SPEED * direction
        else:
            self.velocity[0] = 0  # Stop moving if attention is higher

        self.rect.move_ip(self.velocity)

        # Clamp to screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

        

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(screen, self.fallback_color, self.rect.center, BALL_RADIUS)

    def check_collision(self, other_ball):
        """Handles collision logic between balls."""
        if self.rect.colliderect(other_ball.rect):
            if self.isFrozen:
                # Ensure the frozen ball remains completely still
                self.velocity = [0, 0]  
                
                # Make the other ball bounce away
                other_ball.velocity[0] *= -1  
                other_ball.velocity[1] *= -1  
                other_ball.rect.move_ip(other_ball.velocity)

            elif other_ball.isFrozen:
                # Ensure the other frozen ball remains completely still
                other_ball.velocity = [0, 0]  

                # Make this ball bounce away
                self.velocity[0] *= -1  
                self.velocity[1] *= -1  
                self.rect.move_ip(self.velocity)

            else:
                # Normal bounce logic if neither ball is frozen
                self.velocity, other_ball.velocity = other_ball.velocity, self.velocity
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
