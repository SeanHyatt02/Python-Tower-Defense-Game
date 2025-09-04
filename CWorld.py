import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import random
import CConstants as c

class World():
  def __init__(self, data_list, map_images):
    self.level = 1
    self.health = c.HEALTH
    self.money = c.MONEY  
    self.tile_map = []
    self.waypoints = []
    self.waypoints_alternative = []
    self.number_of_waypoints = 1
    self.level_data_list = data_list
    self.level_data = self.level_data_list[0]
    self.image_list = map_images
    self.image = self.image_list[0]
    self.enemy_list = []
    self.spawned_enemies = 0

  def process_data(self):
    #look through data to extract relevant info
    for layer in self.level_data["layers"]:
      if layer["name"] == "Map":
        self.tile_map = layer["data"]
      elif layer["name"] == "Waypoints":
        self.number_of_waypoints = 1
        for obj in layer["objects"]:
          waypoint_data = obj["polyline"]
          self.process_waypoints(waypoint_data, False)
      elif layer["name"] == "Waypoints2":
        self.number_of_waypoints = 2
        for obj in layer["objects"]:
          waypoint_data = obj["polyline"]
          self.process_waypoints(waypoint_data, True)

  def process_waypoints(self, data, alternative):
    # The alternative variable determines if path is original or branching
    if alternative:
      #iterate through waypoints to extract individual sets of x and y coordinates
      for point in data:
        temp_x = point.get("x")
        temp_y = point.get("y")
        self.waypoints_alternative.append((temp_x, temp_y))
    else:
      for point in data:
        temp_x = point.get("x")
        temp_y = point.get("y")
        self.waypoints.append((temp_x, temp_y))

  def process_images(self, imageNumber):
    # Change the current image
    self.image = self.image_list[imageNumber]
    self.level_data = self.level_data_list[imageNumber]
    self.waypoints.clear()
    self.waypoints_alternative.clear()

  def clear_enemy_list(self):
    self.spawned_enemies = 0
    self.enemy_list.clear()

  def process_enemies(self):
    enemies = ENEMY_SPAWN_DATA[self.level - 1] #spot 0 
    #spawn in enemies from data
    for enemy_type in enemies:
      enemies_to_spawn = enemies[enemy_type]
      for enemy in range(enemies_to_spawn):
        self.enemy_list.append(enemy_type)
    #Now randomize list to shuffle enemy spawning
    random.shuffle(self.enemy_list)

    # Increment list for next wave
    self.level += 1

  def draw(self, surface):
    surface.blit(self.image, (0, 0))