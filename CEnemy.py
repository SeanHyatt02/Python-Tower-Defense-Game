import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images, death_images):
        super().__init__()

        # Load spritesheets and frames for different directions
        self._init_frames(enemy_type, images)
        self._init_death_frames(enemy_type, death_images)

        # Initialize key attributes
        self.frame_index = 0
        self.direction = "down"
        self.image = self.frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(waypoints[0])
        self.pos = Vector2(self.rect.center)

        self.waypoints = waypoints
        self.target_waypoint = 1
        self.speed = ENEMY_DATA[enemy_type]["speed"]
        self.health = ENEMY_DATA[enemy_type]["health"]
        self.value = ENEMY_DATA[enemy_type]["reward"]
        self.attack_damage = ENEMY_DATA[enemy_type]["damage"]
        # Death animation control
        self.is_alive = True
        self.last_update = pg.time.get_ticks()  # Initialize last_update
        self.last_death_update = 0
        self.death_animation_duration = 1500  # Total duration of death animation in ms

        self.sound = pg.mixer.Sound(ENEMY_DATA[enemy_type]["sound"])
        self.evil_laughSfx = pg.mixer.Sound("Assets/Sounds/evil-laugh.mp3")

    def animate(self):
        # Update animation frame at a set interval
        now = pg.time.get_ticks()
        if now - self.last_update > 100:  # Adjust frame rate as needed
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.frame_index]

    def animate_death(self):
        self.is_alive = False  # Set flag to indicate enemy is dead
        self.frame_index = 0  # Start death animation from the first frame
        self.last_death_update = pg.time.get_ticks()

        # Determine the direction of death animation based on the current direction
        death_direction = self.direction
        if death_direction == "right":
            self.death_frames[death_direction] = self.death_frames[death_direction][::-1]  # Reverse the death frames

        # Ensure the direction of the sprite matches the direction of the death animation
        self.image = self.death_frames[death_direction][0]

        #Sounds
        self.sound.set_volume(0.1)
        self.sound.play()

    def _init_frames(self, enemy_type, images):
        frame_width = 48
        frame_height = 48
        rows = 1
        cols = 6

        self.spritesheets = {
            "up": images[enemy_type]["up"],
            "down": images[enemy_type]["down"],
            "left": images[enemy_type]["left"],
            "right": pg.transform.flip(images[enemy_type]["left"], True, False),
        }

        self.frames = {direction: [] for direction in self.spritesheets.keys()}
        for direction, spritesheet in self.spritesheets.items():
            for row in range(rows):
                for col in range(cols):
                    frame = spritesheet.subsurface(
                        (col * frame_width, row * frame_height, frame_width, frame_height)
                    )
                    self.frames[direction].append(frame)

    def _init_death_frames(self, enemy_type, death_images):
        frame_width = 48
        frame_height = 48
        rows = 1
        cols = 6  # Adjust according to your spritesheet's layout

        # Set up the spritesheets for death animations
        self.death_spritesheets = {
            "up": death_images[enemy_type]["up"],
            "down": death_images[enemy_type]["down"],
            "left": death_images[enemy_type]["left"],
            "right": pg.transform.flip(death_images[enemy_type]["left"], True, False),
        }

        # Initialize the dictionary for frames
        self.death_frames = {direction: [] for direction in self.death_spritesheets.keys()}

        # Extract frames from each spritesheet
        for direction, spritesheet in self.death_spritesheets.items():
            for row in range(rows):
                for col in range(cols):
                    death_frame = spritesheet.subsurface(
                        (col * frame_width, row * frame_height, frame_width, frame_height)
                    )
                    self.death_frames[direction].append(death_frame)

        return self.death_frames

    def move(self, playerHealth):
        if self.target_waypoint < len(self.waypoints):
            target_pos = Vector2(self.waypoints[self.target_waypoint])
            movement_vector = target_pos - self.pos
            distance = movement_vector.length()

            if distance > self.speed:
                self.pos += movement_vector.normalize() * self.speed
            else:
                self.pos = target_pos
                self.target_waypoint += 1

            self.rect.center = self.pos
            self.update_direction(movement_vector)
        else:
            # If the enemy has reached the end of the waypoints
            playerHealth.update(self.attack_damage)
            self.kill()
            self.evil_laughSfx.set_volume(0.5)
            self.evil_laughSfx.play()


    def update(self, player_money, player_health, enemiesRemainingCounter):
        if self.is_alive:
            self.move(player_health)
            self.animate()
        else:
            now = pg.time.get_ticks()
            elapsed_time = now - self.last_death_update

            if elapsed_time > self.death_animation_duration:
                self.kill()
            else:
                total_frames = len(self.death_frames[self.direction])
                progress = elapsed_time / self.death_animation_duration
                frame_idx = int(progress * total_frames)
                frame_idx = min(frame_idx, total_frames - 1)  # Avoid out-of-bounds error

                self.image = self.death_frames[self.direction][frame_idx]

        if self.health <= 0 and self.is_alive:
            player_money.update(self.value)  # Reward for killing the enemy
            enemiesRemainingCounter.update_enemy_number(enemiesRemainingCounter.enemies_remaining_number-1)
            self.animate_death()  # Trigger death animation

    def update_direction(self, movement_vector):
        angle = math.degrees(math.atan2(movement_vector[1], movement_vector[0]))

        if -45 < angle <= 45:
            self.direction = "right"
        elif 45 < angle <= 135:
            self.direction = "down"
        elif 135 < angle <= 180 or -180 <= angle < -135:
            self.direction = "left"
        else:
            self.direction = "up"

        self.image = self.frames[self.direction][self.frame_index]


