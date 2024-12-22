import pygame
import sys

pygame.init()

class PokemonBattle:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pokemon Battle")
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (100, 200, 100)
        self.RED = (200, 100, 100)
        
        self.battle_state = {
            "opponent": {
                "name": "SALAMECHE",
                "level": 5,
                "current_hp": 20,
                "max_hp": 20,
                "position": (600, 100)
            },
            "player": {
                "name": "BULBIZARRE",
                "level": 5,
                "current_hp": 20,
                "max_hp": 20,
                "position": (200, 300)
            }
        }
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def draw_hp_bar(self, current_hp, max_hp, position):
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(self.screen, self.GRAY, 
                        (position[0], position[1], bar_width, bar_height))
        
        current_width = (current_hp / max_hp) * bar_width
        pygame.draw.rect(self.screen, self.GREEN, 
                        (position[0], position[1], current_width, bar_height))
        
        pygame.draw.rect(self.screen, self.BLACK, 
                        (position[0], position[1], bar_width, bar_height), 2)

    def draw_pokemon_info(self, pokemon_data, position, is_opponent=False):
        name_text = self.font.render(f"{pokemon_data['name']} Nv.{pokemon_data['level']}", 
                                   True, self.BLACK)
        self.screen.blit(name_text, position)
        
        hp_position = (position[0], position[1] + 30)
        self.draw_hp_bar(pokemon_data['current_hp'], pokemon_data['max_hp'], hp_position)
        
        hp_text = self.small_font.render(f"{pokemon_data['current_hp']}/{pokemon_data['max_hp']} PV", 
                                       True, self.BLACK)
        self.screen.blit(hp_text, (hp_position[0], hp_position[1] + 25))

    def draw_battle_menu(self):
        menu_items = ["ATTAQUE", "SAC", "POKEMON", "FUITE"]
        menu_rect = pygame.Rect(10, self.screen_height - 150, 
                              self.screen_width - 20, 140)
        
        pygame.draw.rect(self.screen, self.WHITE, menu_rect)
        pygame.draw.rect(self.screen, self.BLACK, menu_rect, 2)
        
        for i, item in enumerate(menu_items):
            x = menu_rect.x + 10 + (i % 2) * (menu_rect.width // 2 - 20)
            y = menu_rect.y + 10 + (i // 2) * 60
            
            button_rect = pygame.Rect(x, y, menu_rect.width // 2 - 20, 50)
            pygame.draw.rect(self.screen, self.GRAY, button_rect)
            pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)
            
            text = self.font.render(item, True, self.BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def draw_battle_scene(self):
        self.screen.fill((144, 238, 144)) 
        
        self.draw_pokemon_info(
            self.battle_state["opponent"],
            (500, 50),
            True
        )
        
        self.draw_pokemon_info(
            self.battle_state["player"],
            (50, 250),
            False
        )
        
        self.draw_battle_menu()
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            
            self.draw_battle_scene()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    battle = PokemonBattle()
    battle.run()