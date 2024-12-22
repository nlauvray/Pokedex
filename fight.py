from flask import render_template, request
from pokedex import app
import threading
import pygame
import random
import sys

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arène de Combat Pokémon")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger les images des Pokémon et des arrière-plans
background_image = pygame.image.load("static/arene.svg")  # Ajoutez votre image d'arène ici
pokemon1_image = pygame.image.load("static/bulbasaur.png")  # Ajoutez l'image du Pokémon 1
pokemon2_image = pygame.image.load("static/charmander.png")  # Ajoutez l'image du Pokémon 2

# Redimensionner les sprites
pokemon1_image = pygame.transform.scale(pokemon1_image, (150, 150))
pokemon2_image = pygame.transform.scale(pokemon2_image, (150, 150))

# Classes pour les Pokémon
class Pokemon:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        damage = max(1, self.attack - target.defense + random.randint(-5, 5))  # Variation aléatoire
        target.take_damage(damage)
        return damage

# Créer les Pokémon
bulbasaur = Pokemon("Bulbizarre", 100, 20, 10)
charmander = Pokemon("Salamèche", 100, 25, 8)

def draw_arena():
    screen.blit(background_image, (0, 0))
    screen.blit(pokemon1_image, (50, 400))
    screen.blit(pokemon2_image, (600, 400))

def main():
    clock = pygame.time.Clock()
    running = True
    turn = 0  # 0 = Bulbizarre, 1 = Salamèche

    while running:
        screen.fill(WHITE)
        draw_arena()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gérer les actions de combat
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Espace pour attaquer
                    if turn == 0:  # Bulbizarre attaque
                        damage = bulbasaur.attack_target(charmander)
                        print(f"{bulbasaur.name} inflige {damage} dégâts à {charmander.name}!")
                    else:  # Salamèche attaque
                        damage = charmander.attack_target(bulbasaur)
                        print(f"{charmander.name} inflige {damage} dégâts à {bulbasaur.name}!")

                    turn = 1 - turn  # Changer de tour

        # Vérifier si un Pokémon est KO
        if bulbasaur.hp <= 0 or charmander.hp <= 0:
            winner = "Bulbizarre" if charmander.hp <= 0 else "Salamèche"
            print(f"{winner} gagne le combat!")
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()
    
@app.route('/start_game')
def start_game():
    threading.Thread(target=main).start()
    return "Game started!"