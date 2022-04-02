from pygame import mixer


class Key:
    def __init__(self, key_name: str, file_name: str, channel_id: int) -> None:
        self.key_name = key_name
        self.file_name = file_name
        self.channel_id = channel_id
        self.is_pressed = False

    def play(self, velocity: int = 127) -> None:
        if velocity == 0:
            self.stop()
        else:
            self.is_pressed = True
            note = mixer.Sound(self.file_name)
            mixer.Channel(self.channel_id).set_volume((velocity / 127) * 1)
            mixer.Channel(self.channel_id).play(note)

    def stop(self) -> None:
        self.is_pressed = False
        mixer.Channel(self.channel_id).fadeout(300)
