echo Starting..
pyinstaller --noconsole --add-data "icon.ico;." --onefile --icon icon.ico yeelightControl.pyw
timeout -1