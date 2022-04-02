def create_keymap() -> dict[str, str]:
    keymap = {}

    # Notes that go 0 -> 7
    keymap.update({
        f'{n}{i}': f'notes/{n}{i}.wav' for n in ['a', 'b'] for i in range(8)
    })

    # Notes that go 1 -> 7
    keymap.update({
        f'{n}{i}': f'notes/{n}{i}.wav' for n in ['d', 'e', 'f', 'g'] for i in range(1, 8)
    })

    # Notes that go 1 -> 8
    keymap.update({
        f'{n}{i}': f'notes/{n}{i}.wav' for n in ['c'] for i in range(1, 8)
    })

    # sharps that go 0 -> 7
    keymap.update({
        f'{n}{i}#': f'notes/{n}{i}#.wav' for n in ['a'] for i in range(8)
    })

    # Sharps that go 1 -> 7
    keymap.update({
        f'{n}{i}#': f'notes/{n}{i}#.wav' for n in ['c', 'd', 'f', 'g'] for i in range(8)
    })

    return keymap


def midi_number_to_note(num: int) -> str:
    return {
        21: 'a0', 22: 'a0#', 23: 'b0',
        24: 'c1', 25: 'c1#', 26: 'd1', 27: 'd1#', 28: 'e1', 29: 'f1', 30: 'f1#', 31: 'g1', 32: 'g1#', 33: 'a1', 34: 'a1#', 35: 'b1',
        36: 'c2', 37: 'c2#', 38: 'd2', 39: 'd2#', 40: 'e2', 41: 'f2', 42: 'f2#', 43: 'g2', 44: 'g2#', 45: 'a2', 46: 'a2#', 47: 'b2',
        48: 'c3', 49: 'c3#', 50: 'd3', 51: 'd3#', 52: 'e3', 53: 'f3', 54: 'f3#', 55: 'g3', 56: 'g3#', 57: 'a3', 58: 'a3#', 59: 'b3',
        60: 'c4', 61: 'c4#', 62: 'd4', 63: 'd4#', 64: 'e4', 65: 'f4', 66: 'f4#', 67: 'g4', 68: 'g4#', 69: 'a4', 70: 'a4#', 71: 'b4',
        72: 'c5', 73: 'c5#', 74: 'd5', 75: 'd5#', 76: 'e5', 77: 'f5', 78: 'f5#', 79: 'g5', 80: 'g5#', 81: 'a5', 82: 'a5#', 83: 'b5',
        84: 'c6', 85: 'c6#', 86: 'd6', 87: 'd6#', 88: 'e6', 89: 'f6', 90: 'f6#', 91: 'g6', 92: 'g6#', 93: 'a6', 94: 'a6#', 95: 'b6',
        96: 'c7', 97: 'c7#', 98: 'd7', 99: 'd7#', 100: 'e7', 101: 'f7', 102: 'f7#', 103: 'g7', 104: 'g7#', 105: 'a7', 106: 'a7#', 107: 'b7',
        108: 'c8',
    }[num]
