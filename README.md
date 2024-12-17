# digitaldiary

There are a few ways to run this app at the moment. There is a build file for an .exe, but the solution needs Docker running at the moment, so the .exe doesn't work. 

My current flow is as follows:

The backend is in Python currently, so I use Miniconda and pip install for all package needs. 

You'll need a Docker container running. Then, my normal flow is to start localstack. To run/stop localstack, run: ```localstack start/stop```

I then run ```python main.py``` from the main repo. There's also a barebones Flask app under lib/window. From there, you can run ```flask run``` if you have it installed. 

To build the .exe, run:
```pyinstaller main.spec```

If the icons are messed up, run: ```pyinstaller --onefile --windowed --add-data "icons/;icons" main.py```
