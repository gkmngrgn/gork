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

[1]: https://github.com/connor-makowski/pixelator
[2]: https://github.com/JonnoFTW/img_term
