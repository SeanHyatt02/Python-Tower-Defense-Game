import CConstants as c
import pygame as pg

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.font = None
        self.font_size = 24
        self.alive = True

    def update(self, damage):
        self.current_health -= damage

        if self.current_health <= 0:
            self.alive = False

    def initialize_font(self):
        # Initialize font if not already initialized
        if not self.font:
            pg.font.init()
            self.font = pg.font.Font(None, self.font_size)

    def drawText(self, surface, screen_width):
        # Initialize font if not already initialized
        self.initialize_font()

        health_text = f"Health: {self.current_health}"
        text_surface = self.font.render(health_text, True, c.white)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (screen_width - self.x, self.y)
        surface.blit(text_surface, text_rect)    

    def CheckAlive(self):
        return self.alive

    def draw(self, surface, screen_width):
        # Calculate health bar width based on current health
        health_ratio = self.current_health / self.max_health
        bar_width = int(self.width * health_ratio)

        # Draw health bar outline
        outline_rect = pg.Rect(screen_width - self.x - self.width, self.y, self.width, self.height)
        pg.draw.rect(surface, c.white, outline_rect, 1)

        # Draw health bar filled with red
        health_rect = pg.Rect(screen_width - self.x - self.width, self.y, bar_width, self.height)
        pg.draw.rect(surface, c.red, health_rect)

# Initialize health bar
#player_health = HealthBar(20, 20, 200, 20, 100)

# In the game loop, update and draw the health bar
#player_health.update(80)  # Update health value
#player_health.draw(c.screen,c.SCREEN_WIDTH)  # Draw the health bar on the screen
