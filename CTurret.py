
import os
import pygame as pg
import math
import CConstants as c
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
    def __init__(self, turret_level, tile_x, tile_y, archer_spriteSheets):
        super().__init__()

        # Initialize archer action
        self.archer_action = "Idle"  # Default action
        self.relative_direction = "Up"  # Default relative direction

        #Sound
        self.bow_sfx = pg.mixer.Sound("Assets/Sounds/bow.mp3")

        # Initialize archer visibility based on starting level
        self.archer_visible = False if turret_level in [4, 7] else True


        # Tower Position Variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = self.tile_x * c.TILE_SIZE + c.TILE_SIZE // 2
        self.y = self.tile_y * c.TILE_SIZE + c.TILE_SIZE // 2 - 30

        # Archer Position Variables
        self.archer_tile_x = tile_x
        self.archer_tile_y = tile_y
        self.archer_x = self.archer_tile_x * c.TILE_SIZE + c.TILE_SIZE // 2
        self.archer_y = self.archer_tile_y * c.TILE_SIZE + c.TILE_SIZE // 2

        # Load turret sprite sheet; archer is false
        self.sprite_sheets = self.load_sprite_sheets(False)

        # Load Archer Sprite Sheet; archer is true
        self.archer_sprite_sheets = self.load_sprite_sheets(True)

        # Load images based on turret level
        self.animation_list = []
        for sprite_sheet in self.sprite_sheets:
            self.animation_list.extend(self.load_images(sprite_sheet))

        # Load images based on archer level
        self.archer_animation_list = []
        for sprite_sheet in self.archer_sprite_sheets:
            self.archer_animation_list.extend(self.load_archer_images(sprite_sheet))

        # Turret properties
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.damage = TURRET_DATA[self.upgrade_level - 1].get("damage")
        self.cost = TURRET_DATA[self.upgrade_level - 1].get("cost")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.firing_start_time = None  # Track when the turret begins firing
        self.firing_animation_delay = 600  # Delay duration in milliseconds (adjust as needed)
        self.is_firing = False  # Flag to indicate if the turret is firing
    
        # Animation variables
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.archer_frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.archer_update_time = pg.time.get_ticks()
        self.last_animation_update = pg.time.get_ticks()
        self.archer_last_animation_update = pg.time.get_ticks()

        self.last_archer_update = 0

        # Upgrade animation variables
        self.upgrade_animation = None
        self.upgrade_duration = 300
        self.upgrade_start_time = 0
        self.upgrade_frame_index = 0
        self.is_upgrading = False  # Flag to indicate whether the turret is currently being upgraded
        self.is_upgrade_complete = False  # Flag to indicate whether the upgrade animation has finished

        # Update Tower image
        self.angle = 0
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Update Archer image
        self.archer_angle = 0
        self.archer_original_image = self.archer_animation_list[self.frame_index]
        self.archer_image = pg.transform.rotate(self.archer_original_image, self.angle)


        # Create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        self.range_image.fill((0, 0, 0, 0))
        pg.draw.circle(self.range_image, (169, 169, 169, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = (self.x, self.y + 30)


    def load_sprite_sheets(self, archer):
        # Initialize list
        sprite_sheets = []

        # Find tower sprite sheets
        if archer is False:
            # Path to the directory containing tower sprite sheets
            path = os.path.join("Assets", "TowerAssets", "IdleSheets")

            # List of turret sprite sheet filenames
            filenames = [f"{turret_level}.png" for turret_level in range(1, 8)]

            # Load sprite sheets
            for filename in filenames:
                try:
                    sprite_sheet = pg.image.load(os.path.join(path, filename)).convert_alpha()
                    if sprite_sheet is None:
                        raise ValueError(f"Could not load sprite sheet at {os.path.join(path, filename)}")
                    sprite_sheets.append(sprite_sheet)
                except Exception as e:
                    raise ValueError(f"Error loading sprite sheet at {os.path.join(path, filename)}: {e}")
        # Find archer sprite sheet
        elif archer is True:
            # Path to the directory containing archer sprite sheet
            archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1" , f"{self.relative_direction}{self.archer_action}.png")

            # Load sprite sheets
            try:
                sprite_sheet = pg.image.load(archer_path).convert_alpha()
                if sprite_sheet is None:
                    raise ValueError(f"Could not load sprite sheet at {archer_path}")
                sprite_sheets.append(sprite_sheet)
            except Exception as e:
                raise ValueError(f"Error loading sprite sheet at {archer_path}: {e}")

        return sprite_sheets

    def load_images(self, sprite_sheet):
        animation_list = []
        if sprite_sheet.get_width() == 70:  # Single frame
            animation_list.append(sprite_sheet)
        elif sprite_sheet.get_width() == 280:  # Four-frame spritesheet
            frame_width = sprite_sheet.get_width() // 4
            frame_height = sprite_sheet.get_height()
            for x in range(4):
                temp_img = sprite_sheet.subsurface(pg.Rect(x * frame_width, 0, frame_width, frame_height))
                temp_img = (temp_img)
                animation_list.append(temp_img)
        elif sprite_sheet.get_width() == 420:  # Six-frame spritesheet
            frame_width = sprite_sheet.get_width() // 6
            frame_height = sprite_sheet.get_height()
            for x in range(6):
                temp_img = sprite_sheet.subsurface(pg.Rect(x * frame_width, 0, frame_width, frame_height))
                temp_img = (temp_img)
                animation_list.append(temp_img)
        else:
            print("Unsupported sprite sheet dimensions:", sprite_sheet.get_size())
        return animation_list
    
    # This function splits the archer sprite sheets
    def load_archer_images(self, sprite_sheet):
        animation_list = []
        if sprite_sheet.get_width() == 48:  # Single frame
            animation_list.append(sprite_sheet)
        elif sprite_sheet.get_width() == 192:  # Four-frame spritesheet
            frame_width = sprite_sheet.get_width() // 4
            frame_height = sprite_sheet.get_height()
            for x in range(4):
                temp_img = sprite_sheet.subsurface(pg.Rect(x * frame_width, 0, frame_width, frame_height))
                temp_img = (temp_img)
                animation_list.append(temp_img)
        elif sprite_sheet.get_width() == 288:  # Six-frame spritesheet
            frame_width = sprite_sheet.get_width() // 6
            frame_height = sprite_sheet.get_height()
            for x in range(6):
                temp_img = sprite_sheet.subsurface(pg.Rect(x * frame_width, 0, frame_width, frame_height))
                temp_img = (temp_img)
                animation_list.append(temp_img)
        else:
            print("Unsupported sprite sheet dimensions:", sprite_sheet.get_size())
        return animation_list
    
    def _init_frames(self, archer_images):
        frame_width = 48
        frame_height = 48
        rows = 1
        cols = 6

        self.archer_spritesheets = {
            "Up": archer_images[self.archer_action]["up"],
            "Down": archer_images[self.archer_action]["down"],
            "Left": archer_images[self.archer_action]["left"],
            "Right": archer_images[self.archer_action]["right"],
        }

        image_width = self.archer_spritesheets["Up"].get_width()

        self.archer_frames = {direction: [] for direction in self.archer_spritesheets.keys()}
        for self.archer_action, spritesheet in self.archer_spritesheets.items():
            for row in range(rows):

                if image_width == 48:       # Single image
                    for col in range(cols):
                        frame = spritesheet.subsurface(
                            (col * frame_width, row * frame_height, frame_width, frame_height)
                        )
                        self.archer_frames[self.archer_action].append(frame)
                elif image_width == 192:    # Four-frame spritesheet
                    for col in range(cols):
                        frame = spritesheet.subsurface(
                            (col * frame_width, row * frame_height, frame_width, frame_height)
                        )
                        self.archer_frames[self.archer_action].append(frame)
                elif image_width == 288:    # Six-frame spritesheet
                    for col in range(cols):
                        frame = spritesheet.subsurface(
                            (col * frame_width, row * frame_height, frame_width, frame_height)
                        )
                        self.archer_frames[self.archer_action].append(frame)
                else:
                    print("Unsupported image size")


    def update(self, enemy_group):
        self.update_animation()
        self.update_upgrade_animation()
        self.update_animation_archer()

        # if target picked, play firing animation
        if self.target:
            self.target_reset()
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # Default values for relative_direction and archer_action
        self.relative_direction = "Up"
        self.archer_action = "Idle"
        
        closest_enemy = None
        min_distance = float("inf")
        
        # Find the closest enemy within range
        for enemy in enemy_group:
            if enemy.health > 0:  # Check if the enemy is alive
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y

                # Check for null pointer reference
                if x_dist is None or y_dist is None:
                    continue

                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)  # Calculate distance to the turret

                # Check for unhandled exception
                try:
                    if dist < self.range and dist < min_distance:
                        closest_enemy = enemy
                        min_distance = dist

                        # Calculate relative direction based on the position of the closest enemy
                        if abs(x_dist) > abs(y_dist):
                            self.relative_direction = "Right" if x_dist > 0 else "Left"
                        else:
                            self.relative_direction = "Down" if y_dist > 0 else "Up"
                except Exception as e:
                    print(f"Error calculating distance or relative direction: {e}")
                    continue

        if closest_enemy:
            self.target = closest_enemy
            self.archer_action = "Attack"
            self.firing_start_time = pg.time.get_ticks()  # Set when firing starts

            self.angle = math.degrees(math.atan2(-y_dist, x_dist))  # Calculate the angle toward the target
            
            # Apply damage to the target
            self.target.health -= self.damage
            self.bow_sfx.set_volume(1)
            self.bow_sfx.play()
            # Print relative direction for debugging
            print(f"Enemy is {self.relative_direction} of the turret.")
            

            if self.relative_direction == "Right":
                archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", f"Side{self.archer_action}.png")
                sprite_sheet = pg.image.load(archer_path).convert_alpha()
                sprite_sheet = pg.transform.flip(sprite_sheet, True, False)  # Flip for right direction
            elif self.relative_direction == "Left":
                archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", f"Side{self.archer_action}.png")
                sprite_sheet = pg.image.load(archer_path).convert_alpha()  # No flip needed for left direction
            else:
                archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", f"{self.relative_direction}{self.archer_action}.png")
                sprite_sheet = pg.image.load(archer_path).convert_alpha()  # Load without flipping
            
            self.archer_sprite_sheets = [sprite_sheet]
            self.archer_animation_list = self.load_archer_images(sprite_sheet)  # Update animation list
            self.archer_frame_index = 0  # Reset frame index
            self.target = closest_enemy  # Set the target
    # Animate archer attack
    def animate(self):
        # Update animation frame at a set interval
        now = pg.time.get_ticks()
        if now - self.last_archer_update > 100:  # Adjust frame rate as needed
            self.last_update = now
            self.archer_frame_index = (self.frame_index + 1) % len(self.archer_frames[self.archer_action])
            self.archer_image = self.archer_frames[self.archer_action][self.frame_index]

    def load_upgrade_animation(self):
        upgrade_sheet_path = os.path.join(c.UPGRADE_SHEETS_PATH, f"{self.upgrade_level}.png")
        upgrade_sheet = pg.image.load(upgrade_sheet_path).convert_alpha()
        num_frames = upgrade_sheet.get_width() // c.TOWER_SPRITE_WIDTH
        upgrade_animation = []
        for frame_index in range(num_frames):
            frame_x = frame_index * c.TOWER_SPRITE_WIDTH
            frame_rect = (frame_x, 0, c.TOWER_SPRITE_WIDTH, c.TOWER_SPRITE_HEIGHT)
            frame_image = upgrade_sheet.subsurface(frame_rect)
            upgrade_animation.append(frame_image)
        return upgrade_animation
    
    def upgrade_turret(self):
        if self.upgrade_level < len(TURRET_DATA):
            # Upgrade the turret level
            self.upgrade_level += 1
            
            # Update the turret's properties based on the new upgrade level
            self.damage = TURRET_DATA[self.upgrade_level - 1]['damage']
            self.range = TURRET_DATA[self.upgrade_level - 1]['range']
            self.cooldown = TURRET_DATA[self.upgrade_level - 1]['cooldown']
            self.cost = TURRET_DATA[self.upgrade_level - 1]['cost']

            # Check if the archer should be invisible at certain levels
            if self.upgrade_level in [4, 7]:
                self.archer_visible = False
            else:
                self.archer_visible = True

            # Update the turret's range circle to reflect the new range
            self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
            self.range_image.fill((0, 0, 0, 0))
            pg.draw.circle(self.range_image, (169, 169, 169, 100), (self.range, self.range), self.range)
            self.range_rect = self.range_image.get_rect()
            self.range_rect.center = (self.x, self.y + 30)

            # Start the upgrade animation
            self.upgrade_animation = self.load_upgrade_animation()
            self.upgrade_start_time = pg.time.get_ticks()
            self.is_upgrading = True  # Set the flag indicating the turret is upgrading
            self.is_upgrade_complete = False  # Reset the upgrade completion flag

            # Update archer placement or other adjustments based on the upgrade level
            if self.upgrade_level == 2:
                self.archer_y -= 15
            elif self.upgrade_level == 3:
                self.archer_y -= 10
            
        else:
            # Handle the case when the turret is already at the maximum upgrade level
            print("Max turret level reached")

    def returnUpgrade(self):
        return self.upgrade_level

    def target_reset(self):
        
        if self.firing_start_time is not None and (pg.time.get_ticks() - self.firing_start_time) < self.firing_animation_delay:
            return  # If the firing animation hasn't completed, don't reset to idle
        
        # If the delay has passed, proceed to reset to idle
        self.target = None
        self.last_shot = pg.time.get_ticks()  # Record last shot time for cooldown
        
        # Check if enough time has passed since the firing started
        if self.firing_start_time is not None and (pg.time.get_ticks() - self.firing_start_time) < self.firing_animation_delay:
            return  # Do not transition to idle if the delay has not passed
        

        # Determine which idle sprite sheet to use based on relative direction
        if self.relative_direction == "Right":
            archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", "SideIdle.png")
            sprite_sheet = pg.image.load(archer_path).convert_alpha()  # Load the side idle sprite sheet
            sprite_sheet = pg.transform.flip(sprite_sheet, True, False)  # Flip the sprite for right-facing
        elif self.relative_direction == "Left":
            archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", "SideIdle.png")
            sprite_sheet = pg.image.load(archer_path).convert_alpha()  # Load the side idle sprite sheet
        else:
            archer_path = os.path.join("Assets", "TowerAssets", "UnitsSheets", "Level1", f"{self.relative_direction}Idle.png")
            sprite_sheet = pg.image.load(archer_path).convert_alpha()  # Load the corresponding idle sprite sheet
        
        # Set the sprite sheet and reset animation
        self.archer_sprite_sheets = [sprite_sheet]  # Update the sprite sheet
        self.archer_animation_list = self.load_archer_images(sprite_sheet)  # Reload the animation list
        self.archer_frame_index = 0  # Reset the frame index
        
        # Set the archer action to idle
        self.archer_action = "Idle"

    def update_animation(self):
        if not self.is_upgrading:  # Only update the animation if not currently upgrading
            self.update_time = pg.time.get_ticks()
            # Adjust the animation speed separately from the firing rate
            animation_speed = 200  # Adjust this value to control the animation speed (lower value = faster animation)
            if self.update_time - self.last_animation_update > animation_speed:
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list):
                    self.frame_index = 0
                self.last_animation_update = self.update_time
                self.image = self.animation_list[self.frame_index]

    def update_animation_archer(self):
        if not self.is_upgrading:
            current_time = pg.time.get_ticks()
            animation_speed = 150  # 150ms per frame
            
            if current_time - self.archer_last_animation_update > animation_speed:
                self.archer_frame_index = (self.archer_frame_index + 1) % len(self.archer_animation_list)  # Cycle frames
                
                # Ensure correct orientation for Right direction
                if self.relative_direction == "Right":
                    sprite_sheet = self.archer_sprite_sheets[0]
                    sprite_sheet = pg.transform.flip(sprite_sheet, True, False)  # Flip for right-facing
                    self.archer_sprite_sheets[0] = sprite_sheet
                
                # Update the image with the new frame
                self.archer_image = self.archer_animation_list[self.archer_frame_index]
                self.archer_last_animation_update = current_time  # Update the last update time


    def update_upgrade_animation(self):
        if self.is_upgrading:
            current_time = pg.time.get_ticks()
            elapsed_time = current_time - self.upgrade_start_time
            if elapsed_time >= self.upgrade_duration * len(self.upgrade_animation):
                self.is_upgrading = False  # Upgrade animation finished
                self.is_upgrade_complete = True  # Upgrade animation complete
                
                # Update animation list and original image to match the new upgrade level
                self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
                self.original_image = self.animation_list[self.frame_index]
                
            else:
                frame_index = elapsed_time // self.upgrade_duration
                if frame_index != self.upgrade_frame_index:
                    self.upgrade_frame_index = frame_index
                    self.image = self.upgrade_animation[self.upgrade_frame_index]
    


    def draw(self, surface):
        # Draw the turret regardless of upgrade level
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)

        if self.selected:
            surface.blit(self.range_image, self.range_rect)

        # Only draw the archer if visible
        if self.archer_visible:
            self.archer_rect = self.archer_image.get_rect()
            self.archer_rect.center = (self.archer_x, self.archer_y)
            surface.blit(self.archer_image, self.archer_rect)
