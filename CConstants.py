import pygame as pg

ROWS = 15
COLS = 15
TILE_SIZE = 48
SIDE_PANEL = 300
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FULLSCREEN_WIDTH = SCREEN_WIDTH + SIDE_PANEL
FPS = 60
screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_PANEL, SCREEN_HEIGHT))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

#turret constants
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
TURRET_LEVELS = 7
BUY_COST = 200
UPGRADE_COST = 100
KILL_REWARD = 1
DAMAGE = 5

#Enemy constants
SPAWN_COOLDOWN = 400

HEALTH = 100
MONEY = 650

# Alert popups in milliseconds
MESSAGE_ALERT = 2000

# Menu selection delay
MENU_DELAY = 100


# Constants for TowerAssets directory structure
IDLE_SHEETS_PATH = "Assets/TowerAssets/IdleSheets/"
UNIT_SHEETS_PATH = "Assets/TowerAssets/UnitsSheets/"
UPGRADE_SHEETS_PATH = "Assets/TowerAssets/UpgradeSheets/"

# Constants for sprite sheet dimensions
TOWER_SPRITE_WIDTH = 70
TOWER_SPRITE_HEIGHT = 130
ARCHER_SPRITE_WIDTH = 48
ARCHER_SPRITE_HEIGHT = 48

