echo Creating executable...
pyinstaller GameLauncher.spec

echo Created executable.
echo Creating res directory...

xcopy /s /y /f src\res dist\res
rem     xcopy /y /f src\res dist\res

echo Created res directory.

rem echo Zipping res directory...
rem python zipResources.py
rem echo Zip complete.

pause