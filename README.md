# snake-py

Python implementation of snake.

## Development - Getting Started

1. Open a shell at this repository.
2. `poetry install`
3. `poetry shell`
4. `code .`

Assuming the Python extension is enabled/installed, you should now be able to build.

## Package for Distribution

```bash
nuitka --onefile --plugin-enable=pylint-warnings --include-package-data=pygame_gui.data --include-data-dir=data=data -o package/Snake.exe --output-dir=package src/snake/__main__.py
```
