import pygame
import os
from Ball import Ball
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED,BLUE
from EEG import EEGDevice
from SkillEventManager import SkillEventManager

class Scene_Game:
    def __init__(self,scene_manager):
        print("GameInit")
        self.eegDevice = None
        self.scene_manager = scene_manager
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brainball Collision Game")
        self.clock = pygame.time.Clock()
        self.running = False

        # Load font
        self.font = pygame.font.Font(None, 36)  # Default pygame font, size 36
        
        # Load balls
        self.ball1 = Ball(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, "pop_cat.png", RED, {
            'left': pygame.K_a, 'right': pygame.K_d,
            'up': pygame.K_w, 'down': pygame.K_s,
            'Skill_1':pygame.K_1,'Skill_2':pygame.K_2,'Skill_1':pygame.K_3
        })
        self.ball2 = Ball(2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, "brainball2.png", BLUE, {
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'up': pygame.K_UP, 'down': pygame.K_DOWN,
            'Skill_1':pygame.K_KP1,'Skill_2':pygame.K_KP2,'Skill_1':pygame.K_KP3
        })

    def ConnectEEGDEVICE(self,port):
        
        if self.eegDevice is None:
            self.eegDevice = EEGDevice(port)

    
    
    
    def run(self):
        
        #print(f"Starting game with {self.eegDevice.ser.port}...")
        #while self.running:
            
        self.handle_events()
        self.update()
        self.draw()
        self.eegDevice.fetch_data()
        self.clock.tick(60)



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.scene_manager.switch_scene("Menu")  # Switch back to menu

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.scene_manager.switch_scene("Menu")  # Exit to menu when ESC is pressed

                
    def update(self):
        keys = pygame.key.get_pressed()
        #self.ball1.move_based_on_focus(self.eegDevice.avg_meditation,self.eegDevice.avg_attention,False)
        self.ball1.move(keys)
        self.ball2.move(keys)

        self.ball1.use_skill(keys)
        self.ball2.use_skill(keys)
        
        self.ball1.GetSkillHolder().regenerate_mana()
        self.ball2.GetSkillHolder().regenerate_mana()
        # Check for collision between the two balls
        self.ball1.check_collision(self.ball2)

    def draw(self):
        self.screen.fill(WHITE)
        self.ball1.draw(self.screen)
        self.ball2.draw(self.screen)
        # Render EEG Text
        meditation_text = self.font.render(f"Meditation: {self.eegDevice.avg_meditation}", True, (0, 0, 0))
        attention_text = self.font.render(f"Attention: {self.eegDevice.avg_attention}", True, (0, 0, 0))
                # Blit the text to the screen
        self.screen.blit(meditation_text, (20, 20))
        self.screen.blit(attention_text, (20, 60))
        pygame.display.flip()
