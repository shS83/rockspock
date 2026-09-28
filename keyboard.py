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

_input_fd = None
_owns_tty_fd = None

def setup_keyboard():
    global _old_terminal_settings

    if os.name == "nt":
        return

    fd = _get_unix_fd()

    _old_terminal_settings = termios.tcgetattr(fd)

    # Parempi terminaalipelille kuin setraw():
    tty.setcbreak(fd)


def _get_unix_fd():
    global _input_fd, _owns_tty_fd

    if _input_fd is not None:
        return _input_fd

    if sys.stdin.isatty():
        _input_fd = sys.stdin.fileno()
    else:
        _input_fd = os.open("/dev/tty", os.O_RDONLY)
        _owns_tty_fd = True

    return _input_fd


def restore_keyboard():
    global _old_terminal_settings
    global _input_fd
    global _owns_tty_fd

    if os.name == "nt":
        return

    if _old_terminal_settings is not None and _input_fd is not None:
        termios.tcsetattr(
            _input_fd,
            termios.TCSADRAIN,
            _old_terminal_settings,
        )

    if _owns_tty_fd and _input_fd is not None:
        os.close(_input_fd)

    _old_terminal_settings = None
    _input_fd = None
    _owns_tty_fd = False


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
    fd = _get_unix_fd()

    ready, _, _ = select.select([fd], [], [], 0)

    if not ready:
        return None

    key = os.read(fd, 1)

    if key == b"\x1b":
        # ESC voi olla itsenäinen ESC tai nuolinäppäimen alku.
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