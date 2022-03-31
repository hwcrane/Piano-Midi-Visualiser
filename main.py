from key import *
from piano import Piano
import pygame as pg
from mido import MidiFile
from keymap import midi_number_to_note
import sys

pg.init()
display = pg.display.set_mode((1, 1))
pg.mixer.set_num_channels(100)
pg.display.update()
p = Piano()

file = sys.argv[1]
mid = MidiFile(file)
for msg in mid:
    pg.time.delay(round(msg.time * 1000))
    if not msg.is_meta:
        print(msg)
        if msg.type == "note_on":
            p.play_key(midi_number_to_note(msg.note), msg.velocity)
        elif msg.type == "note_off":
            p.stop_key(midi_number_to_note(msg.note))
