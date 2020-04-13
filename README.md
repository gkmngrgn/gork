# GORK

I derived the name from Zork that is a first text-based adventure game.

```
poetry install
poetry run gork --help
```

![](files/b_output.jpg)

The terminal output:

[![asciicast](https://asciinema.org/a/284169.svg)](https://asciinema.org/a/284169)

The base calculation code is from [pixelator][1] project. Also [img_term][2] app
helped me to display the image in the terminal.

# Contributing

```
poetry run pytest

# to generate report
poetry run coverage run -m pytest
poetry run coverage report -m
```

# TODO

- ~~Add a new feature to print the 8bit image in the terminal.~~
- ~~Print the color palette in the terminal.~~
- Print metadata of images.
- ~~Use mypy for the static typing.~~
- Use async for the performance improvements.
- Configure GitHub actions for the tests.
- Generate a self-contained executable file with PyOxidizer.
- Generate random palettes, to find the best colors.
- Recognize the object and texts in the images.

[1]: https://github.com/connor-makowski/pixelator
[2]: https://github.com/JonnoFTW/img_term
