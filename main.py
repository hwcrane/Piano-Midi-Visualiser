from threading import Thread

from numpy.lib.function_base import blackman
from key import *
from piano import Piano
import pygame as pg
from mido import MidiFile
from keymap import midi_number_to_note
import sys
from piano_roll import PianoRoll


class Main:
    def __init__(self) -> None:
        self.time = 0
        self.running = True
        self.clock = pg.time.Clock()
        self.song_name = self.get_song_name()

        self.midiFile = self.load_midi_file()
        self.display = self.setup_pygame(self.song_name)

        self.background = self.create_background()
        self.piano = Piano()
        self.piano_roll = PianoRoll(self.midiFile)

    def setup_pygame(self, songName: str):
        pg.init()
        display = pg.display.set_mode((1248, 500))
        pg.display.set_caption(f'Playing: {songName}')
        pg.mixer.set_num_channels(100)
        return display

    def get_song_name(self):
        return sys.argv[1]

    def load_midi_file(self):
        file = sys.argv[1]
        return MidiFile(file, clip=True)

    def play_notes(self):
        for msg in self.midiFile:
            if not self.running:
                return
            if not msg.is_meta:
                divider = round(10 + msg.time * 100)
                for _ in range(divider):
                    pg.time.delay(round((msg.time * 1000) / divider))
                    self.time += msg.time / divider
                if msg.type == "note_on":
                    self.piano.play_key(
                        midi_number_to_note(msg.note), msg.velocity)
                elif msg.type == "note_off":
                    self.piano.stop_key(midi_number_to_note(msg.note))

        pg.time.delay(2000)
        self.running = False

    def create_background(self):
        background = pg.Surface((1248, 500))
        background.fill((255, 255, 0))
        image = pg.image.load('doodad.png')
        background.blit(image, (0, 0))
        return background

    def mainloop(self):

        # Start playing midi File in separate Thread
        thread = Thread(target=self.play_notes)
        thread.start()

        # Pygame Main loop
        while self.running:
            self.clock.tick(50)

            # Calculate piano roll offaet
            offset = self.time * 100 + 400

            # Update screen
            self.display.blit(self.background, (0, 0))
            self.piano_roll.draw(self.display, offset)
            self.piano.draw_keys(self.display)
            pg.display.flip()

            # Check if window closed
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        # Makes sure thread has stopped before ending program
        if thread.is_alive():
            thread.join()


if __name__ == '__main__':
    Main().mainloop()

    pg.quit()
