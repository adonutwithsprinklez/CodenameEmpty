echo Creating executable...
pyinstaller --onefile --clean --noconsole^
    -n GameLauncher ^
    GameLauncher.spec

echo Created executable.
echo Creating res directory...

rem xcopy /s /y /f src\res dist\res
xcopy /y /f src\res dist\res

echo Created res directory.
echo Zipping res directory...

python zipResources.py

echo Zip complete.
pause