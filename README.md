# snake-py

Python implementation of snake.

## Package for Distribution

```bash
nuitka --onefile --plugin-enable=numpy --plugin-enable=pylint-warnings --windows-disable-console -o package/Snake.exe --output-dir=package --remove-output src/snake/__main__.py
```
