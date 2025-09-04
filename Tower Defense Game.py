import pygame as pg
import sys
from CEnemy import Enemy
from CWorld import World
from CTurret import Turret
from CButton import Button
import CConstants as c
import json
import CHealth as hp
import CMoney as mo
import CRoundInfo as RoundInfo
from turret_data import TURRET_DATA
from pygame.transform import flip

#TEST
# Initialize Pygame
pg.init()
pg.font.init()
# Set clock
clock = pg.time.Clock()

# Get the screen dimensions
screen_info = pg.display.Info()

#Load fonts for displaying text ons creen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

# Create the main screen
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense Game")

# Game variables
placing_turrets = False
last_enemy_spawn = pg.time.get_ticks()

# Credits text import
credits_doc = open("Assets/credits.txt", 'r')
#credits_text = credits_doc.read()

#for line in credits_text:
    #credits_lines.extend(line)


#Sound Variables
buy_turretSfx = pg.mixer.Sound("Assets/Sounds/buy-turret.wav")
sell_turretSfx = pg.mixer.Sound("Assets/Sounds/sell-turret.wav")
no_moneySfx = pg.mixer.Sound("Assets/Sounds/no-money.mp3")
round_completeSfx = pg.mixer.Sound("Assets/Sounds/victory.mp3")
main_menuSfx = pg.mixer.Sound("Assets/Sounds/Credits_Loop.wav")
upgrade_turretSfx = pg.mixer.Sound("Assets/Sounds/upgrade.wav")


world_data_list = []

# Load images
# Map
map_image = pg.image.load('Map/Map-0/Map-0.png').convert_alpha()
map_image_list = []
for map in range(0, 5):
    map_image = pg.image.load(f'Map/Map-{map}/Map-{map}.png').convert_alpha()
    #map_image = pg.image.load('Map/Map-4/Map-4.png').convert_alpha()
    map_image_list.append(map_image)

    with open(f'Map/Map-{map}/level.tmj') as file:
    #with open('Map/Map-4/level.tmj') as file:
        world_data = json.load(file)
        world_data_list.append(world_data)

#Enemy images 
#enemy_image = pg.image.load('Assets//Enemies/enemy_1.png').convert_alpha()
# Enemy images 

# Load the left sprite for each enemy type
left_sprite_slime = pg.image.load('Assets/Monster Assets/Slime/SideWalk.png').convert_alpha()
left_sprite_wolf = pg.image.load('Assets/Monster Assets/Wolf/SideWalk.png').convert_alpha()
left_sprite_goblin = pg.image.load('Assets/Monster Assets/Goblin/SideWalk.png').convert_alpha()
left_sprite_hornet = pg.image.load('Assets/Monster Assets/Hornet/SideWalk.png').convert_alpha()

# Flip the left sprite horizontally to create the right sprite for each enemy type
right_sprite_slime = flip(left_sprite_slime, True, False)
right_sprite_wolf = flip(left_sprite_wolf, True, False)
right_sprite_goblin = flip(left_sprite_goblin, True, False)
right_sprite_hornet = flip(left_sprite_hornet, True, False)

# Define the enemy_images dictionary
enemy_images = {
    "weak": {
        "up": pg.image.load('Assets/Monster Assets/Slime/UpWalk.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Slime/DownWalk.png').convert_alpha(),
        "left": left_sprite_slime,
        "right": right_sprite_slime
    },
    "medium": {
        "up": pg.image.load('Assets/Monster Assets/Wolf/UpWalk.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Wolf/DownWalk.png').convert_alpha(),
        "left": left_sprite_wolf,
        "right": right_sprite_wolf
    },
    "strong": {
        "up": pg.image.load('Assets/Monster Assets/Goblin/UpWalk.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Goblin/DownWalk.png').convert_alpha(),
        "left": left_sprite_goblin,
        "right": right_sprite_goblin
    },
    "elite": {
        "up": pg.image.load('Assets/Monster Assets/Hornet/UpWalk.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Hornet/DownWalk.png').convert_alpha(),
        "left": left_sprite_hornet,
        "right": right_sprite_hornet
    }
}

# Load the left death sprite for each enemy type
left_death_sprite_slime = pg.image.load('Assets/Monster Assets/Slime/SideDeath.png').convert_alpha()
left_death_sprite_wolf = pg.image.load('Assets/Monster Assets/Wolf/SideDeath.png').convert_alpha()
left_death_sprite_goblin = pg.image.load('Assets/Monster Assets/Goblin/SideDeath.png').convert_alpha()
left_death_sprite_hornet = pg.image.load('Assets/Monster Assets/Hornet/SideDeath.png').convert_alpha()

# Flip the left death sprite horizontally to create the right death sprite for each enemy type
right_death_sprite_slime = flip(left_death_sprite_slime, True, False)
right_death_sprite_wolf = flip(left_death_sprite_wolf, True, False)
right_death_sprite_goblin = flip(left_death_sprite_goblin, True, False)
right_death_sprite_hornet = flip(left_death_sprite_hornet, True, False)

##
death_images = {
    "weak": {
        "up": pg.image.load('Assets/Monster Assets/Slime/UpDeath.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Slime/DownDeath.png').convert_alpha(),
        "left": left_death_sprite_slime,
        "right": right_death_sprite_slime
    },
    "medium": {
        "up": pg.image.load('Assets/Monster Assets/Wolf/UpDeath.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Wolf/DownDeath.png').convert_alpha(),
        "left": left_death_sprite_wolf,
        "right": right_death_sprite_wolf
    },
    "strong": {
        "up": pg.image.load('Assets/Monster Assets/Goblin/UpDeath.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Goblin/DownDeath.png').convert_alpha(),
        "left": left_death_sprite_goblin,
        "right": right_death_sprite_goblin
   },
    "elite": {
        "up": pg.image.load('Assets/Monster Assets/Hornet/UpDeath.png').convert_alpha(),
        "down": pg.image.load('Assets/Monster Assets/Hornet/DownDeath.png').convert_alpha(),
        "left": left_death_sprite_hornet,
        "right": right_death_sprite_hornet
    }
}


#turret spritesheet
#turret_sheet = pg.image.load('Assets/Turrets/turret_1.png').convert_alpha()
#Individual Turret
cursor_turret = pg.image.load('Assets/TowerAssets/IdleSheets/cursor_turret.png').convert_alpha()
# Load turret sprite sheets
turret_spriteSheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'Assets/TowerAssets/UpgradeSheets/{x}.png').convert_alpha()
    turret_spriteSheets.append(turret_sheet)


# Archer images
# Placed onto the towers
archer_spriteSheets = []

# Load the left sprite for each archer type
left_idle_archer = pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/SideIdle.png').convert_alpha()
left_preattack_archer = pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/SidePreattack.png').convert_alpha()
left_attack_archer = pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/SideAttack.png').convert_alpha()

# Flip the left sprite horizontally to create the right sprite for each enemy type
right_idle_archer = flip(left_sprite_slime, True, False)
right_preattack_archer = flip(left_sprite_wolf, True, False)
right_attack_archer = flip(left_sprite_goblin, True, False)

# Define the enemy_images dictionary
archer_images = {
    "idle": {
        "up": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/UpIdle.png').convert_alpha(),
        "down": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/DownIdle.png').convert_alpha(),
        "left": left_idle_archer,
        "right": right_idle_archer
    },
    "preattack": {
        "up": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/UpPreattack.png').convert_alpha(),
        "down": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/DownPreattack.png').convert_alpha(),
        "left": left_preattack_archer,
        "right": right_preattack_archer
    },
    "attack": {
        "up": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/UpAttack.png').convert_alpha(),
        "down": pg.image.load('Assets/TowerAssets/UnitsSheets/Level1/DownAttack.png').convert_alpha(),
        "left": left_attack_archer,
        "right": right_attack_archer
    }
}


archer_sheet = pg.image.load(f'Assets/TowerAssets/UnitsSheets/Level1/SideAttack.png').convert_alpha()
archer_spriteSheets.append(turret_sheet)

# Button Images
buy_turret_image = pg.image.load('Assets/Buttons/buy_turret.png')
cancel_image = pg.image.load('Assets/Buttons/cancel.png')
upgrade_turret_image = pg.image.load('Assets/Buttons/upgrade.png')
sell_turret_image = pg.image.load('Assets/Buttons/sell.png')
begin_round_image = pg.image.load('Assets/Buttons/begin.png')
main_menu_image = pg.image.load('Assets/Buttons/main_menu.png')
fast_forward_image = pg.image.load('Assets/Buttons/fast_forward.png')
normal_speed_image = pg.image.load('Assets/Buttons/normal_speed.png') 

# Level Select Thumbnails
map0_thumbnail = pg.image.load('Map/Map-0/Map-0_thumbnail.png')
map1_thumbnail = pg.image.load('Map/Map-1/Map-1_thumbnail.png')
map2_thumbnail = pg.image.load('Map/Map-2/Map-2_thumbnail.png')
map3_thumbnail = pg.image.load('Map/Map-3/Map-3_thumbnail.png')
map4_thumbnail = pg.image.load('Map/Map-4/Map-4_thumbnail.png')


# Create world
world = World(world_data_list, map_image_list)
world.process_data()
world.process_enemies()

# Create Groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
archer_group = pg.sprite.Group()


# Create game buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 65, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 65, 180, upgrade_turret_image, True)
sell_button = Button (c.SCREEN_WIDTH + 65, 240, sell_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 30, 525, begin_round_image, True)
return_main_menu_button = Button(c.SCREEN_WIDTH + 30, 600, main_menu_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 30, 450, fast_forward_image, True)
normal_speed_button = Button(c.SCREEN_WIDTH + 30, 525, normal_speed_image, True)

# Create level select buttons
map0_button = Button(200, 300, map0_thumbnail, True)
map1_button = Button(450, 300, map1_thumbnail, True)
map2_button = Button(700, 300, map2_thumbnail, True)
map3_button = Button(325, 500, map3_thumbnail, True)
map4_button = Button(575, 500, map4_thumbnail, True)

#Output text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)


def create_turret(mouse_pos, playerMoney):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

  # Grab turret cost
  turretCost = int(TURRET_DATA[0].get("cost"))

  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  
  #check to see if tile is grass
  if world.tile_map[mouse_tile_num] == 1:
    #Check to see if a turret is already there
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
        #no_moneySfx.play()
    if space_is_free == True and (playerMoney.returnValue() - turretCost) >= 0:
      new_turret = Turret(turret_spriteSheets, mouse_tile_x, mouse_tile_y, archer_images)
      # Purchase turret
      playerMoney.update(-turretCost)
      buy_turretSfx.set_volume(0.5)
      buy_turretSfx.play()
      turret_group.add(new_turret)
    elif space_is_free:
        no_moneySfx.set_volume(0.6)
        no_moneySfx.play()
  else:
    no_moneySfx.set_volume(0.6)
    no_moneySfx.play()

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #Check to see if turret there
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
         return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

def draw_text(text, font, color, x, y):
# Function to display text on the screen
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    

# This function sets the original values for the round to restart the game
def OriginalValues():
    # Remove all current enemies and turrets from map
    for enemy in enemy_group:
        enemy.kill()
    for turret in turret_group:
        turret.kill()
        
    # Rerun the enemy creation
    world.process_enemies()
    world.process_images(0)
    world.process_data()


# Main menu loop
def main_menu():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(pg.mouse.get_pos()):
                    #OriginalValues()
                    #game_screen()
                    pg.time.delay(c.MENU_DELAY)
                    level_select_screen()
                elif credits_button_rect.collidepoint(pg.mouse.get_pos()):
                    credit_screen()                    
                elif quit_button_rect.collidepoint(pg.mouse.get_pos()):
                    credits_doc.close()
                    pg.quit()
                    sys.exit()


        main_menuSfx.set_volume(0.1)
        main_menuSfx.play()

        screen.fill(c.black)
        draw_text("Tower Defense", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 2 - 10, c.SCREEN_HEIGHT // 4)

        # Start button
        start_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH // 4 + 150, c.SCREEN_HEIGHT // 2, 200, 50))
        draw_text("Start Game", pg.font.Font(None, 36), c.black, start_button_rect.centerx, start_button_rect.centery)

        # Quit button
        quit_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH // 4 + 150, c.SCREEN_HEIGHT // 2 + 100, 200, 50))
        draw_text("Quit Game", pg.font.Font(None, 36), c.black, quit_button_rect.centerx, quit_button_rect.centery)

        # Credits button
        credits_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH - 250, c.SCREEN_HEIGHT - 100, 200, 50))
        draw_text("Credits", pg.font.Font(None, 36), c.black, credits_button_rect.centerx, credits_button_rect.centery)

        pg.display.flip()

# This function is the credit screen for the main menu
def credit_screen():
    screen.fill(c.black)

    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if main_menu_button_rect.collidepoint(pg.mouse.get_pos()):
                    main_menu()

        main_menuSfx.set_volume(0.1)
        main_menuSfx.play()

        draw_text("Credits", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 2 - 10, 50)

        credits = RoundInfo.RoundInformation()
        credits.draw_credits(screen, credits_doc)

        # Go Back button
        main_menu_button_rect = pg.draw.rect(screen, c.white, (30, 20, 200, 50))
        draw_text("Go Back", pg.font.Font(None, 36), c.black, main_menu_button_rect.centerx, main_menu_button_rect.centery)

        #print(credits_text)

        pg.display.flip()


# Level select menu
def level_select_screen():
    map_increment_yes_button_rect = pg.draw.rect(screen, c.white, (0, 0, 200, 50))
    map_increment_no_button_rect = pg.draw.rect(screen, c.white, (0, 0, 200, 50))
    mapIncrement = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if map_increment_yes_button_rect.collidepoint(pg.mouse.get_pos()):
                    mapIncrement = True

                if mapIncrement == True:
                    if map_increment_no_button_rect.collidepoint(pg.mouse.get_pos()):
                        mapIncrement = False


        main_menuSfx.set_volume(0.1)
        main_menuSfx.play()

        screen.fill(c.black)
        draw_text("Please Select a Level", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 2 - 10, c.SCREEN_HEIGHT // 4)

        if mapIncrement == False:
            # Map Progress Button
            map_increment_yes_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH - 250, c.SCREEN_HEIGHT - 100, 200, 50))
            draw_text("Progress Maps", pg.font.Font(None, 36), c.black, map_increment_yes_button_rect.centerx, map_increment_yes_button_rect.centery)
        
        elif mapIncrement == True:
            # Map Progress Button
            map_increment_no_button_rect = pg.draw.rect(screen, c.white, (40, c.SCREEN_HEIGHT - 100, 200, 50))
            draw_text("Stationary Map", pg.font.Font(None, 36), c.black, map_increment_no_button_rect.centerx, map_increment_no_button_rect.centery)

        if map0_button.draw(screen):
            map = 0
            world.process_images(map)
            world.process_data()

            game_screen(map, mapIncrement)
        
        elif map1_button.draw(screen):
            map = 1
            world.process_images(map)
            world.process_data()

            game_screen(map, mapIncrement)
        
        elif map2_button.draw(screen):
            map = 2
            world.process_images(map)
            world.process_data()

            game_screen(map, mapIncrement)
        
        elif map3_button.draw(screen):
            map = 3
            world.process_images(map)
            world.process_data()

            game_screen(map, mapIncrement)
        
        elif map4_button.draw(screen):
            map = 4
            world.process_images(map)
            world.process_data()

            game_screen(map, mapIncrement)
        
        pg.display.flip()

# Game screen loop
def game_screen(mapNumber, mapIncrement):
    # Initialize health bar and currency display
    playerMoney = mo.Money(130, 20, 24, 100)
    player_health = hp.HealthBar(110, 55, 200, 20, 100)
    roundCounter = RoundInfo.RoundInformation()
    enemiesRemainingCounter = RoundInfo.RoundInformation()

    main_menuSfx.stop()

    #mapNumber = 0
    # Load turret sprite sheets
    turret_spriteSheets = [
        pg.image.load(c.UPGRADE_SHEETS_PATH + "1.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "2.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "3.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "4.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "5.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "6.png").convert_alpha(),
        pg.image.load(c.UPGRADE_SHEETS_PATH + "7.png").convert_alpha()
    ]

    # Game loop variables
    selected_turret = None
    spawnEnemy = False
    allEnemySpawn = False
    fastForward = False
    beginRound = True

    # Global variables
    global last_enemy_spawn
    global placing_turrets

     # Inside the game loop
    for turret in turret_group:
        screen.blit(turret.animation_list[turret.animation_list], turret.rect.topleft)
    
    for archer in archer_group:
        screen.blit(archer.archer_animation[archer.archer_animation_list], archer.rect.topleft)
        
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    main_menu()
            #elif event.type == pg.MOUSEBUTTONDOWN:
                #if return_button_rect.collidepoint(pg.mouse.get_pos()):
                    #main_menu()

        if fastForward == True:
            clock.tick(c.FPS * 3)
        else:
            # Set frame rate
            clock.tick(c.FPS)

        ###################
        # UPDATING SECTION
        ###################

        # Group update
        enemy_group.update(playerMoney, player_health, enemiesRemainingCounter)
        turret_group.update(enemy_group)
        archer_group.update(enemy_group)
        

        ###################
        # DRAWING SECTION
        ###################

        # Draw window background color
        screen.fill(c.black)

        # Draw world map
        world.draw(screen)

        # Draw game information displays
        playerMoney.draw(screen, c.SCREEN_WIDTH + 160)
        player_health.drawText(screen, c.SCREEN_WIDTH + 141)
        roundCounter.draw_round_number(screen)
        enemiesRemainingCounter.draw_enemy_number(screen)


        # Draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)


        if spawnEnemy == True:
            #Spawn Enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                #As long as there is still enemies, spawn them
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]

                    # Branch paths if there is more than one path
                    if world.number_of_waypoints > 1:
                        # Enemies split at a 50/50 ratio
                        if world.spawned_enemies % 2 == 0:
                            enemy = Enemy(enemy_type, world.waypoints, enemy_images, death_images)
                        else:
                            enemy = Enemy(enemy_type, world.waypoints_alternative, enemy_images, death_images)
                    else:
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images, death_images)

                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()
                else:
                    allEnemySpawn = True

            # Hide begin round button
            beginRound = False

        # Update number of enemies before each round
        if beginRound != False:
            # Update enemy remaining number
            enemiesRemainingCounter.update_enemy_number(len(world.enemy_list))

        # Draw speed buttons
        if fastForward == False and spawnEnemy == True:
            if fast_forward_button.draw(screen):
                fastForward = True

        if fastForward == True:
            if normal_speed_button.draw(screen):
                fastForward = False

        # Draw begin round button if there are no enemies
        if beginRound == True:
            if begin_button.draw(screen):
                # Pause to ensure fast forward button is not hit on accident
                pg.time.delay(100)
                spawnEnemy = True
                placing_turrets = False
                
        # Button for placing turrets
        if turret_button.draw(screen):
            placing_turrets = True

        # if placing turrets then show the cancel button as well
        if placing_turrets == True:
            # Show curser turret
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

        #If a turret is selected, show upgrade button
        if selected_turret:
            #If a turret can be upgraded, show upgrade button
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                if upgrade_button.draw(screen):
                    # Find the level of turret
                    level = selected_turret.returnUpgrade()
                    # Find price of upgrade
                    upgradeCost = int(TURRET_DATA[level].get("cost"))

                    # Check to see if you can upgrade
                    if playerMoney.returnValue() > upgradeCost:
                        selected_turret.upgrade_turret()
                        upgrade_turretSfx.set_volume(0.7)
                        upgrade_turretSfx.play()
                        # Subtract money 
                        playerMoney.update(-upgradeCost)
                    else:
                        no_moneySfx.play()
            
            # Also show the sell button as well
            if sell_button.draw(screen):
                # Find level of turret
                level = selected_turret.returnUpgrade()
                # Find selling value of turret
                sellValue = int(TURRET_DATA[level-1].get("value"))

                playerMoney.update(sellValue)
                sell_turretSfx.play()
                selected_turret.kill()
                selected_turret = False

        #draw_text("ROUND COMPLETE!", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 3, c.SCREEN_HEIGHT // 4)

        # if all enemies are dead then end round
        if len(enemy_group) == 0 and allEnemySpawn == True:
            # Print "Round Complete" on screen
            draw_text("ROUND COMPLETE!", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 3, 
                      c.SCREEN_HEIGHT // 4)
            round_completeSfx.set_volume(0.4)
            round_completeSfx.play()
            
            pg.display.flip()

            # Wait designated milliseconds before continuing
            pg.time.delay(c.MESSAGE_ALERT)

            roundCounter.increase_round()

            if mapIncrement == True:
                mapNumber += 1
                for turret in turret_group:
                    turret.kill()

            # Reset game state for the next round
            world.clear_enemy_list()
            world.process_images(mapNumber)
            world.process_data()
            world.draw(screen)
            world.process_enemies()

            allEnemySpawn = False
            spawnEnemy = False
            fastForward = False
            beginRound = True

        # If player runs out of health, end game
        if player_health.CheckAlive() == False:
            game_over()

        # Button that returns to main menu
        if return_main_menu_button.draw(screen):
            main_menu()

        # Event handler
        for event in pg.event.get():
            #Mouse Click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()

                #check if mouse is on game area
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    #clear selected turret
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        #check for enough money for turret here
                        create_turret(mouse_pos, playerMoney)
                        
                    else:
                        selected_turret = select_turret(mouse_pos)

        # Return to main menu button
        #return_button_rect = pg.draw.rect(screen, c.white, (800, 600, 200, 50))
        #draw_text("Return to Main Menu", pg.font.Font(None, 24), c.black, return_button_rect.centerx, return_button_rect.centery)

        pg.display.flip()

# Game Over loop
def game_over():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(pg.mouse.get_pos()):
                    OriginalValues()
                    game_screen()
                elif quit_button_rect.collidepoint(pg.mouse.get_pos()):
                    pg.quit()
                    sys.exit()

        screen.fill(c.black)
        draw_text("GAME OVER!!!", pg.font.Font(None, 74), c.white, c.FULLSCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 4)
        draw_text("PLAY AGAIN?", pg.font.Font(None, 50), c.white, c.FULLSCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 4 + 60)


        # Start button
        restart_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH // 4 + 150, c.SCREEN_HEIGHT // 2, 200, 50))
        draw_text("Restart Game", pg.font.Font(None, 36), c.black, restart_button_rect.centerx, restart_button_rect.centery)

        # Quit button
        quit_button_rect = pg.draw.rect(screen, c.white, (c.FULLSCREEN_WIDTH // 4 + 150, c.SCREEN_HEIGHT // 2 + 100, 200, 50))
        draw_text("Quit Game", pg.font.Font(None, 36), c.black, quit_button_rect.centerx, quit_button_rect.centery)

        pg.display.flip()

# Run the main menu loop
main_menu()
