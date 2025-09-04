import CConstants as c
import pygame as pg

class Money:
    def __init__(self, x, y, font_size, currentValue):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font = None  # Initialize font as None initially
        self.currentValue = currentValue
        self.currency = 100

    def initialize_font(self):
        # Initialize font if not already initialized
        if not self.font:
            pg.font.init()
            self.font = pg.font.Font(None, self.font_size)

    def update(self, amount):
        self.currentValue += amount

    def returnValue(self):
        return self.currentValue

    def draw(self, surface, screen_width):
        # Initialize font if not already initialized
        self.initialize_font()

        currency_text = f"Currency: {self.currentValue}"
        text_surface = self.font.render(currency_text, True, c.white)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (screen_width - self.x, self.y)
        surface.blit(text_surface, text_rect)

# Initialize currency display
#currency_display = CurrencyDisplay(20, 60, 24)
