# snake-py

Python implementation of snake.

## Development - Getting Started

1. Install poetry
    Windows:

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -`
    ```

    Unix:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Open a shell at this repository.
3. `poetry install`
4. `poetry shell`
5. `code .`

Assuming the Python extension is enabled/installed, you should now be able to build.

## Package for Distribution

> Note that this still currently does not work. 😭

```bash
nuitka --onefile --plugin-enable=pylint-warnings --include-package-data=pygame_gui.data --include-data-dir=data=data -o package/Snake.exe --output-dir=package src/snake/__main__.py
```
