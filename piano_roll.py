import pygame as pg
from mido import MidiFile
from keymap import midi_number_to_note


class PianoRoll:
    def __init__(self, midiFile: MidiFile) -> None:
        self.transcribed_song = self.transcribe_song(midiFile)
        self.surface = self.draw_all_notes_to_surface()
        self.height = self.surface.get_height()

    def draw(self, surface: pg.surface.Surface, offset: float) -> None:
        surface.blit(self.surface, (0, -self.height + offset))

    def transcribe_song(self, song: MidiFile) -> list[tuple[str, float, float]]:
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

    def draw_all_notes_to_surface(self) -> pg.surface.Surface:

        black_dict = {
            'c': 2, 'd': 3, 'f': 5, 'g': 6, 'a': 7
        }

        white_dict = {
            'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'a': 7, 'b': 8
        }

        surface_height = round(self.transcribed_song[-1][2] * 100) + 500
        surface = pg.Surface((1248, surface_height))
        surface.set_colorkey((255, 255, 255))
        surface.fill((42, 42, 42))
        for i in range(8):
            pg.draw.line(surface, (60, 60, 60),
                         (48 + 7 * i * 24, 0), (48 + 7 * i * 24, surface_height))

        for (note, start, end) in self.transcribed_song:
            s = round(start * 100)
            nend = round(end * 100)
            length = max(nend - s, 10)
            nstart = surface_height - s - length

            if note[-1] == '#':
                if note == 'a0#':
                    pg.draw.rect(surface, (255, 255, 255), (16, nstart, 14, length),
                                 border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0), (16, nstart, 14, length),
                                 width=2, border_radius=5)
                else:
                    pg.draw.rect(surface, (255, 255, 255), (16 + 24 * black_dict[note[0]] + 24 * 7 * (int(note[1]) - 1), nstart, 14, length),
                                 border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0), (16 + 24 * black_dict[note[0]] + 24 * 7 * (int(note[1]) - 1), nstart, 14, length),
                                 width=2, border_radius=5)
            else:
                if note == 'a0':
                    pg.draw.rect(surface, (255, 255, 255),
                                 (0, nstart, 24, length), border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (0, nstart, 24, length), width=2, border_radius=5)
                elif note == 'b0':
                    pg.draw.rect(surface, (255, 255, 255),
                                 (24, nstart, 24, length), border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (24, nstart, 24, length), width=2, border_radius=5)
                else:
                    pg.draw.rect(surface, (255, 255, 255), (24 * white_dict[note[0]] + (
                        int(note[1]) - 1) * 24 * 7, nstart, 24, length), border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0), (24 * white_dict[note[0]] + (
                        int(note[1]) - 1) * 24 * 7, nstart, 24, length), width=2, border_radius=5)
        return surface


def index_of_note(note, arr) -> int:
    for i, n in enumerate(arr):
        if n[0] == note:
            return i
    return -1
