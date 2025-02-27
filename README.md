# digitaldiary

There are a few ways to run this app at the moment. There is a build file for an .exe, but the solution needs Docker running at the moment, so the .exe doesn't work. 

My current flow is as follows:

The backend is in Python currently, so I use Miniconda and pip install for all package needs. 

To build Flask: run ```pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --hidden-import boto3 --name server app.py``` from app/backend.

To build the Electron desktop window, run: ```npx electron-packager . MyFlaskApp --platform=win32 --arch=x64 --out=dist --overwrite``` from app/frontend. Then you can just run the .exe file and everything should open! Yay. ```.\dist\MyFlaskApp-win32-x64\MyFlaskApp.exe```
