from threading import Thread
from key import *
from piano import Piano
import pygame as pg
from mido import MidiFile
from keymap import midi_number_to_note
import sys


class C:
    def __init__(self):
        self.time = 0


def play_notes():
    for msg in mid:
        if not running:
            return
        if not msg.is_meta:
            for _ in range(10):
                pg.time.delay(round(msg.time * 100))
                counter.time += msg.time / 10
            if msg.type == "note_on":
                p.play_key(midi_number_to_note(msg.note), msg.velocity)
            elif msg.type == "note_off":
                p.stop_key(midi_number_to_note(msg.note))


def transcribe_song(song: MidiFile):
    # [note, start_time, end_time]
    note_history = []
    # [note, start_time]
    playing_notes = []

    time = 0
    for msg in song:
        if not msg.is_meta:
            time += msg.time
            if msg.type == "note_off" or msg.type == "note_on" and msg.velocity == 0:
                note = midi_number_to_note(msg.note)
                note_index = index_of_note(note, playing_notes)
                if note_index >= 0:
                    played_note = playing_notes.pop(note_index)
                    played_note.append(time)
                    note_history.append(played_note)
            elif msg.type == "note_on":
                note = midi_number_to_note(msg.note)
                playing_notes.append([note, time])
    return note_history


def draw_all_notes_to_surface(notes):

    black_dict = {
        'c': 2, 'd': 3, 'f': 5, 'g': 6, 'a': 7
    }

    white_dict = {
        'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'a': 7, 'b': 8
    }

    surface_height = round(notes[-1][2] * 100)
    surface = pg.Surface((1248, surface_height))
    for (note, start, end) in notes:
        s = round(start * 100)
        nend = round(end * 100)
        length = nend - s
        nstart = surface_height - s - length

        if note[-1] == '#':
            if note == 'a0#':
                pg.draw.rect(surface, (0, 0, 255), (16, nstart, 14, length),
                             border_radius=5)
            else:
                pg.draw.rect(surface, (0, 0, 255), (16 + 24 * black_dict[note[0]] + 24 * 7 * (int(note[1]) - 1), nstart, 14, length),
                             border_radius=5)
        else:
            if note == 'a0':
                pg.draw.rect(surface, (0, 255, 0),
                             (0, nstart, 24, length), border_radius=5)
            elif note == 'b0':
                pg.draw.rect(surface, (0, 255, 0),
                             (24, nstart, 24, length), border_radius=5)
            else:
                pg.draw.rect(surface, (0, 255, 0), (24 * white_dict[note[0]] + (
                    int(note[1]) - 1) * 24 * 7, nstart, 24, length), border_radius=5)
    return surface


def index_of_note(note, arr) -> int:
    for i, n in enumerate(arr):
        if n[0] == note:
            return i
    return -1


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode((1248, 500))

    pg.mixer.set_num_channels(100)
    p = Piano()
    p.draw_keys(display)
    pg.display.update()
    file = sys.argv[1]
    mid = MidiFile(file)
    notes = draw_all_notes_to_surface(transcribe_song(mid))
    clock = pg.time.Clock()

    counter = C()
    running = True

    thread = Thread(target=play_notes)
    thread.start()

    while running:
        clock.tick(50)

        offset = counter.time * 100 + 400

        display.fill((0, 0, 0))
        display.blit(notes, (0, -notes.get_height() + offset))
        p.draw_keys(display)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    if thread.is_alive():
        thread.join()
    pg.quit()
