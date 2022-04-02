from key import Key
from keymap import create_keymap
import pygame as pg
from threading import Thread


class Piano:
    def __init__(self) -> None:
        self.keys = self.load_keys()
        self.white_key_surface, self.black_key_surface = self.create_key_surfaces()
        self.white_pressed_surface = pg.surface.Surface(
            (1248, 100), pg.SRCALPHA, 32).convert_alpha()
        self.black_pressed_surface = pg.surface.Surface(
            (1248, 100), pg.SRCALPHA, 32).convert_alpha()

    def draw_keys(self, surface):
        self.draw_pressed()
        surface.blit(self.white_key_surface, (0, 400))
        surface.blit(self.white_pressed_surface, (0, 400))
        surface.blit(self.black_key_surface, (0, 400))
        surface.blit(self.black_pressed_surface, (0, 400))
        pg.display.update()

    def draw_pressed(self):
        self.white_pressed_surface.fill((0, 0, 0, 0))
        self.black_pressed_surface.fill((0, 0, 0, 0))
        black_dict = {
            'c': 2, 'd': 3, 'f': 5, 'g': 6, 'a': 7
        }
        white_dict = {
            'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'a': 7, 'b': 8
        }
        pressed_colour = (213, 50, 66, 200)

        for key in self.keys.items():
            if key[1].is_pressed:
                # Checks if is a sharp note
                if key[0][-1] == '#':
                    if key[0] == 'a0#':
                        pg.draw.rect(self.black_pressed_surface, pressed_colour, (16, 0, 14, 70),
                                     border_radius=5)
                    else:
                        pg.draw.rect(self.black_pressed_surface, pressed_colour, (16 + 24 * black_dict[key[0][0]] + 24 * 7 * (int(key[0][1]) - 1), 0, 14, 70),
                                     border_radius=5)
                else:
                    if key[0] == 'a0':
                        pg.draw.rect(self.white_pressed_surface,
                                     pressed_colour, (0, 0, 24, 100), border_radius=5)
                    elif key[0] == 'b0':
                        pg.draw.rect(self.white_pressed_surface,
                                     pressed_colour, (24, 0, 24, 100), border_radius=5)
                    else:
                        pg.draw.rect(self.white_pressed_surface,
                                     pressed_colour, (24 * white_dict[key[0][0]] + (int(key[0][1]) - 1) * 24 * 7, 0, 24, 100), border_radius=5)

    def create_key_surfaces(self):
        white_keys = pg.surface.Surface(
            (1248, 100))
        black_keys = pg.surface.Surface(
            (1248, 100), pg.SRCALPHA, 32).convert_alpha()
        for i in range(52):
            pg.draw.rect(white_keys, (200, 200, 200), (i * 24, 0, 24, 100),
                         border_radius=5)
            pg.draw.rect(white_keys, (255, 255, 255), (i * 24, 0, 24, 93),
                         border_radius=5)
            pg.draw.rect(white_keys, (0, 0, 0), (i * 24, 0, 24, 100),
                         width=1, border_radius=5)

        for i in range(50):
            if i not in [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46]:
                pg.draw.rect(black_keys, (150, 150, 150), (i * 24 + 16, 0, 14, 68),
                             border_bottom_left_radius=2, border_bottom_right_radius=2)
                pg.draw.rect(black_keys, (0, 0, 0), (i * 24 + 16 + 2, 0, 10, 70),
                             border_bottom_left_radius=2, border_bottom_right_radius=2)

        return (white_keys, black_keys)

    def play_key(self, key_name: str, velocity) -> None:
        # thread = Thread(target=self.keys[key_name].play, args=[velocity])
        # thread.start()
        self.keys[key_name].play(velocity)

    def stop_key(self, key_name: str) -> None:
        # thread = Thread(target=self.keys[key_name].stop)
        # thread.start()
        self.keys[key_name].stop()

    def load_keys(self) -> dict[str, Key]:
        keymap = create_keymap()

        return {
            k: Key(k, keymap[k], i) for i, k in enumerate(keymap)
        }
