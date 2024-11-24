# digitaldiary

To build the .exe, run:
```pyinstaller main.spec```

If the icons are messed up, run: ```pyinstaller --onefile --windowed --add-data "icons/;icons" main.py```

To run/stop localstack, run: ```localstack start/stop```