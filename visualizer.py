import json
import os
from sys import argv

import pync
from pynput import keyboard


def parse_hotkeys(
    file: str = argv[1] if len(argv) > 1 else os.path.realpath("hotkeys.json"),
) -> dict:
    """
    Parse a list of JSON objects containing hotkey names, descriptions, and a set of keys to activate

    Parameters:
    ---------
        file - the hotkey file, stored in "hotkeys.json" by default

    Returns:
    -------
        a dict containing attributes
            "name" - the name of the shortcut/hotkey combo
            "description" - the purpose of the hotkey
            "keys" - the keys pressed to activate the hotkey
    """
    with open(file) as f:
        hotkeys = json.load(f)
        for hotkey in hotkeys:
            hotkey["keys"] = set(hotkey["keys"])
    return hotkeys


hotkeys = parse_hotkeys()


def format_key(key: str) -> str:
    """
    Convert a key into the format necessary for keyboard.HotKey.parse()
    e.g. ctrl -> <ctrl>, a -> a

    Parameters:
    ----------
        key - the key to be converted
    Returns:
    --------
        the formatted key
    """
    return key if len(key) == 1 else f"<{key}>"


def parse_key(key: keyboard.Key) -> str:
    """
    extract the actual key value from a keyboard.Key object
    """
    try:
        return f"{key.char}"
    except AttributeError:
        return f"{key.name}"


def normalize_hotkey(hotkey: dict) -> str:
    return "+".join(format_key(key) for key in hotkey["keys"])


def send_notification(hotkey):
    if not hotkeys.get(hotkey):
        for hk in hotkeys:
            if normalize_hotkey(hk) == hotkey:
                hotkey = hk
                break
    pync.notify(
        title=hotkey["name"],
        subtitle="+".join(hotkey["keys"]),
        message=hotkey["description"],
        ignoreDnD=True,
        appIcon="",
    )


global_hotkeys = {
    normalize_hotkey(hotkey): lambda: send_notification(hotkey) for hotkey in hotkeys
}
print(global_hotkeys)
with keyboard.GlobalHotKeys(global_hotkeys) as h:
    h.join()
