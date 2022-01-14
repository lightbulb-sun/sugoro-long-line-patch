# Sugoro Quest Long Line Patch

This patch fixes a few overly long lines in AlanMidas's translation of the NES game Sugoro Quest.

## Download
The latest release can be found on the
[releases page](https://github.com/lightbulb-sun/sugoro-long-line-patch/releases).
Patch the translated ROM with one of the `.bsdiff` or `.ips` files
to create the fixed ROM.

## Building
Place the translated ROM into the working directory as `english.nes` and run `python3 patch-sugoro.py`. This script applies the changes from the file `changes.txt` to the final ROM in `fixed.nes`.

## License
Distributed under the MIT License. See LICENSE for more information.
