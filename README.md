# vidtoolz-zoomtext

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-zoomtext.svg)](https://pypi.org/project/vidtoolz-zoomtext/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-zoomtext?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-zoomtext/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-zoomtext/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-zoomtext/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-zoomtext/blob/main/LICENSE)

Zoom out the video and display text as caption.

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-zoomtext
```
## Usage

type ``vid zoomtext --help`` to get help

```bash
usage: vid zoomtext [-h] [-t TEXT] [-f FONT] [-o OUTPUT] [-fs FONTSIZE]
                    [-pad PADDING] [-tc TEXT_COLOR]
                    main_video

Zoom out the video and display text as caption.

positional arguments:
  main_video            Path to the main video file.

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to write
  -f FONT, --font FONT  Font name to use. Ex Noteworthy, Melno, Papyrus,
                        Zapfino (default: Arial)
  -o OUTPUT, --output OUTPUT
                        Output video file name (default: None)
  -fs FONTSIZE, --fontsize FONTSIZE
                        Fontsize (default: 80)
  -pad PADDING, --padding PADDING
                        Padding (default: 80)
  -tc TEXT_COLOR, --text-color TEXT_COLOR
                        Text color. (default: white)

```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-zoomtext
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
