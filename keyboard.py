import os
import sys

KEY_LEFT = "LEFT"
KEY_RIGHT = "RIGHT"
KEY_ENTER = "ENTER"
KEY_ESCAPE = "ESCAPE"

_old_terminal_settings = None

if os.name == "nt":
    import msvcrt

else:
    import select
    import termios
    import tty


def setup_keyboard():
    global _old_terminal_settings

    if os.name == "nt":
        return

    fd = sys.stdin.fileno()
    _old_terminal_settings = termios.tcgetattr(fd)
    tty.setraw(fd)


def restore_keyboard():
    global _old_terminal_settings

    if os.name == "nt":
        return

    if _old_terminal_settings is not None:
        termios.tcsetattr(
            sys.stdin.fileno(),
            termios.TCSADRAIN,
            _old_terminal_settings,
        )

        _old_terminal_settings = None


def read_key_windows():
    if not msvcrt.kbhit():
        return None

    key = msvcrt.getwch()

    # Windowsin extended keys:
    # ensimmäinen merkki on \x00 tai \xe0,
    # toinen kertoo varsinaisen näppäimen.
    if key in ("\x00", "\xe0"):
        key2 = msvcrt.getwch()

        if key2 == "K":
            return KEY_LEFT

        if key2 == "M":
            return KEY_RIGHT

        return None

    if key == "\r":
        return KEY_ENTER

    if key == "\x1b":
        return KEY_ESCAPE

    return key


def read_key_unix():
    fd = sys.stdin.fileno()

    ready, _, _ = select.select([fd], [], [], 0)

    if not ready:
        return None

    key = os.read(fd, 1)

    if key == b"\x1b":
        # Tarkista onko kyseessä ESC vai escape sequence.
        ready, _, _ = select.select([fd], [], [], 0.01)

        if ready:
            key += os.read(fd, 2)

            if key == b"\x1b[D":
                return KEY_LEFT

            if key == b"\x1b[C":
                return KEY_RIGHT

        return KEY_ESCAPE

    if key in (b"\r", b"\n"):
        return KEY_ENTER

    try:
        return key.decode()

    except UnicodeDecodeError:
        return None


def read_key():
    if os.name == "nt":
        return read_key_windows()

    return read_key_unix()