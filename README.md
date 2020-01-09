# Shortcut Visualizer

basic macOS utility to specify a set of application shortcuts to be visualized with a description if applicable

## Defining a Hotkey File

Hotkey files are defined using Javascript Object Notation (JSON). For example, let's look at `hotkey.json`.

```json
[
    {
        "name": "hotkey1",
        "description": "does some stuff",
        "keys": [ "cmd", "shift", "a" ]
    },
    {
        "name": "hotkey2",
        "description": "does some other stuff",
        "keys": [ "cmd", "shift", "b" ]
    }
]
```

`[]` specifies a list of items.  `{}` specifies an object. We have a list of shortcut objects with attributes `name`, `description`, and `keys` (which is a list within the object). These objects are comma separated.

## Using the Visualizer

You'll need python3 installed. You can do this with `brew install python3`. Additionally, we'll need to clone the repository and install necessary dependencies.

```bash
git clone https://github.com/kclejeune/shortcut-visualizer.git
cd shortcut-visualizer
pip3 install -r requirements.txt
```

From the same directory, run the file with

```bash
python3 visualizer.py
```

If you want to use a different hotkey file, you can do so by specifying the file as the first argument to the script.

```bash
python3 visualizer.py [file]
```
