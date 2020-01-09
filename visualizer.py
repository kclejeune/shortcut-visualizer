import json
import os
from sys import argv

import pync
from pynput import keyboard


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
    if "_" in key:
        key = key[: key.index("_")]
    return key if len(key) == 1 else f"<{key}>"


def normalize(keys: list, modifiers: list = ["ctrl", "alt", "shift", "cmd"]) -> str:
    keys.sort(
        key=lambda k: (modifiers.index(k) if k in modifiers else len(modifiers), str(k))
    )
    return "+".join(format_key(key) for key in keys)


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
            hotkey["keys"] = normalize(hotkey["keys"])
    return hotkeys


def handle_hotkey_press(hotkey: str):
    print(hotkey)
    pync.notify(
        title=hotkey["keys"].replace("<", "").replace(">", ""),
        subtitle=hotkey["name"],
        message=hotkey["description"],
        ignoreDnD=True,
        appIcon="",
    )


def monitor_input():
    def on_press(key):
        try:
            print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            print("special key {0} pressed".format(key))

    def on_release(key):
        print("{0} released".format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    global_hotkeys = {
        hotkey["keys"]: lambda: handle_hotkey_press(hotkey)
        for hotkey in parse_hotkeys()
    }
    global_hotkeys["<esc>"] = exit

    with keyboard.GlobalHotKeys(global_hotkeys) as h:
        h.join()
