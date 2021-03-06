# minecraft-mod-manager

[![Latest PyPI version](https://img.shields.io/pypi/v/minecraft-mod-manager.svg)](https://pypi.python.org/pypi/minecraft-mod-manager)

Install and update mods from CurseForge (and possibly other places in the future) through a simple command.

Currently works best with fabric mods.

## Features

- Searches on CurseForge for installed mods to see if there are any updates.
- Filter updates
  - Stable (default), beta `--beta`, or alpha `--alpha` releases.
  - Minecraft version `-v 1.16.4`

## Usage

```
Install or update Minecraft mods from Curseforge.

positional arguments:
  {install,update,configure,list}
                        Install (NOT IMPLEMENTED YET), update, configure, or list mods
  mods
                        The mods to install, update, or configure.
                        If no mods are specified during an update, all mods will be updated.
                        To specify the download site for the mod, put 'curse:' before the mod.
                        E.g. 'curse:litematica'
                        By default it searches all sites for the mod.
                        To configure an alias for the mod, use 'mod_name=ALIAS_NAME'.
                        E.g. 'dynmap=dynmapforge'


minecraft:
  -d DIR, --dir DIR     Location of the mods folder. By default it's the current directory
  -v MINECRAFT_VERSION, --minecraft-version MINECRAFT_VERSION
                        Only update mods to this Minecraft version. Example: -v 1.16.4
  --allow-beta          Allow beta releases
  --allow-alpha         Allow alpha and beta releases

logging & help:
  -h, --help            show this help message and exit
  --debug               Turn on debug messages
```

## Installation

1. Install with `$ pip install --user minecraft-mod-manager`
1. Install `chromedriver`
   - Linux: Install it through your distribution's package manager
   - Windows/OSX:
     - Install Google Chrome if you haven't already
     - Check your [Chrome version](chrome://settings/help)
     - Goto https://chromedriver.chromium.org/downloads

## Authors

- Matteus Magnusson, senth.wallace@gmail.com
