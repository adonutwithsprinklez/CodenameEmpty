pyinstaller --onefile --clean --noconsole^
    -n GameLauncher ^
    GameLauncher.spec

xcopy /s /y /f src\res dist\res
pause