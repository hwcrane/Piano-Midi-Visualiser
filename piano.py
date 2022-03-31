from key import Key
from keymap import create_keymap
from pygame import time
from threading import Thread


class Piano:
    def __init__(self) -> None:
        self.keys = self.load_keys()

    def press_key(self, key_name: str, duration: int) -> None:
        self.play_key(key_name, 127)
        time.delay(duration)
        self.stop_key(key_name)

    def press_key_asyc(self, key_name: str, duration: int) -> None:
        thread = Thread(target=self.press_key, args=(key_name, duration))
        thread.start()
        thread.join()

    def play_key(self, key_name: str, velocity) -> None:
        self.keys[key_name].play(velocity)

    def stop_key(self, key_name: str) -> None:
        self.keys[key_name].stop()

    def load_keys(self) -> dict[str, Key]:
        keymap = create_keymap()

        return {
            k: Key(k, keymap[k], i) for i, k in enumerate(keymap)
        }
