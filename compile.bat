pyinstaller --onefile --clean ^
    -n GameLauncher ^
    src/main.py

xcopy /s /y /f src\res dist\res
pause