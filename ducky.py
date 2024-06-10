import pygame
import math
import random

class ducky():
    def __init__(self, window, image, position, quack_image):
        self.window = window
        self.image = image
        self.quack_image = quack_image
        self.angle = 0
        self.speed = 1
        self.quack_timer = 0
        self.current_sprite = 0
        self.flip = False
        self.position = pygame.Vector2(position)
        self.target_position = pygame.Vector2(500, 500)  
        window.blit(image, position)

    def move_to_next_location(self, move):
        if move:
            direction = self.target_position - self.position
            self.angle = math.degrees(math.atan2(direction.y, direction.x))

            radians = math.radians(self.angle)
            horizontal = math.cos(radians) * self.speed
            vertical = math.sin(radians) * self.speed
            distance_to_target = direction.length()

            if distance_to_target > self.speed:
                self.position.x += horizontal
                self.position.y += vertical
            else:
                self.position = self.target_position
                self.target_position = self.get_random_position(move)

            if horizontal < 0:
                new_image = pygame.transform.flip(self.image, True, False)
                self.flip = True
            elif horizontal > 0:
                new_image = pygame.transform.flip(self.image, False, False)
                self.flip = False

            self.window.blit(new_image, self.position)

        else:
            self.position = self.get_random_position(move)
            new_image = pygame.transform.flip(self.image, self.flip, False)
            self.window.blit(new_image, self.position)

    def get_random_position(self, move):
        if move:
            random_position = pygame.Vector2(
                random.randint(0, self.window.get_width() - self.image.get_width()),
                random.randint(0, self.window.get_height() - self.image.get_height())
            )
            return random_position
        else:
            mouse_position = pygame.mouse.get_pos()
            return pygame.Vector2(mouse_position) - (50, 50)
    
    def play_animation(self, sprite_array, anim_speed):
        self.current_sprite += anim_speed
        if self.current_sprite >= len(sprite_array):
            self.current_sprite = 0
        self.image = sprite_array[int(self.current_sprite)]

    def play_quack_sound(self, sound, quack_angry_audio):
        if not pygame.mixer.get_busy() :
            if self.quack_timer > 5:
                if quack_angry_audio:
                    quack_angry_audio.play()
            else:
                if sound:
                    sound.play()
    
    def quack_is_angry(self, quack, allow_angry_quack):
        self.quack_timer += 0.025
        if allow_angry_quack:
            if quack and self.quack_timer > 5:
                radius = 500
                rand_x = self.position.x + random.randint(-radius, radius)
                rand_y = self.position.y + random.randint(-radius, radius)
                self.window.blit(self.quack_image, (rand_x, rand_y))
        else:
            self.quack_timer = 0
            