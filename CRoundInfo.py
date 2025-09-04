import pygame
import CWorld as World
import CConstants as c

class RoundInformation:
    def __init__(self):
        # Iteration for round number
        self.round_number = 1
        # Counter for remaining enemies
        self.enemies_remaining_number = 0

        # Font Definitions
        self.font = pygame.font.SysFont(None, 24)
        self.text_color = (255, 255, 255)
        self.screen_width = c.SCREEN_WIDTH + c.SIDE_PANEL
        self.screen_height = c.SCREEN_HEIGHT

    def increase_round(self):
        self.round_number += 1
    
    def update_enemy_number(self, enemiesRemainingNumber):
        self.enemies_remaining_number = enemiesRemainingNumber

    def draw_round_number(self, screen):
        round_text = self.font.render(f"Round: {self.round_number}", True, self.text_color)
        round_text_rect = round_text.get_rect()
        round_text_rect.midleft = (self.screen_width - 80, 20)
        screen.blit(round_text, round_text_rect)
    
    def draw_enemy_number(self, screen):
        enemy_text = self.font.render(f"Enemies Remaining: {self.enemies_remaining_number}", True, self.text_color)
        enemy_text_rect = enemy_text.get_rect()
        enemy_text_rect.midleft = (self.screen_width - 269, 90)
        screen.blit(enemy_text, enemy_text_rect)

    def draw_credits(self, screen, credits):
        credit_lines = []

        # Starting place for the top of credits
        text_y = 100

        while True:
            credit_line = credits.readline()[0:-1]

            if not credit_line:
                break

            credit_text = self.font.render(credit_line, True, self.text_color)
            credit_text_rect = credit_text.get_rect()
            credit_text_rect.midleft = (25, text_y)
            screen.blit(credit_text, credit_text_rect)

            # Space in between lines
            text_y += 28
