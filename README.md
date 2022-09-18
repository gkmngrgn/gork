# GORK

I derived the name from Zork that is a first text-based adventure game.

```shell
poetry install
poetry run gork --help

# colors, texts, recognitions, etc
poetry run gork analyze --input=./files/park.png \
                        --output=./files/park_report.txt

# default width, terminal width scale it by height.
poetry run gork print --width=80 \
                      --input=./files/park.png

# default pixel size is 10.
poetry run gork export ./files/park.png \
                       ./files/park_output.png \
                       --pixel-size=15
```

| Original                             | Pixelated                                   |
|--------------------------------------|---------------------------------------------|
| ![](examples/emoji_disappointed.png) | ![](examples/emoji_disappointed_output.png) |
| ![](examples/emoji_heart.png)        | ![](examples/emoji_heart_output.png)        |
| ![](examples/emoji_watermelon.png)   | ![](examples/emoji_watermelon_output.png)   |
| ![](examples/building.png)           | ![](examples/building_output.png)           |
| ![](examples/park.png)               | ![](examples/park_output.png)               |

The terminal output:

[![asciicast](https://asciinema.org/a/284169.svg)](https://asciinema.org/a/284169)

The base calculation code is from [pixelator][1] project. Also [img_term][2] app
helped me to display the image in the terminal.

# Contributing

```shell
poetry poe test
poetry run pytest
```

[1]: https://github.com/connor-makowski/pixelator
[2]: https://github.com/JonnoFTW/img_term
