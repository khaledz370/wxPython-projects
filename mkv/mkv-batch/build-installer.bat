@echo off
setlocal EnableExtensions
rem ---------------------------------------------------------------------------
rem  MKV Batch - build the release .exe and an installer for C:\Program Files
rem
rem    build-installer.bat           build exe + setup (Inno Setup)
rem    build-installer.bat install   build exe, then install it directly into
rem                                  "C:\Program Files\MKV Batch" (asks for admin)
rem
rem  Needs: Rust (https://rustup.rs) with the MSVC toolchain.
rem         Inno Setup 6 (https://jrsoftware.org/isdl.php) for the setup file.
rem ---------------------------------------------------------------------------

set "ROOT=%~dp0"
set "APPNAME=MKV Batch"
set "EXE=%ROOT%src-tauri\target\release\mkv-batch.exe"
set "DIST=%ROOT%dist"

rem version = the "version" line of Cargo.toml
for /f "tokens=2 delims== " %%v in ('findstr /b /c:"version" "%ROOT%src-tauri\Cargo.toml"') do if not defined VERSION set "VERSION=%%~v"
if not defined VERSION set "VERSION=2.0.0"

echo.
echo === MKV Batch %VERSION% ===
echo.

where cargo >nul 2>nul
if errorlevel 1 (
  echo [x] cargo not found. Install Rust from https://rustup.rs and run this again.
  goto :fail
)

rem Cap the build at half the CPU threads so the PC stays usable.
set /a JOBS=%NUMBER_OF_PROCESSORS% / 2
if %JOBS% LSS 1 set JOBS=1

echo [1/3] Building release exe (%JOBS% build jobs)...
pushd "%ROOT%src-tauri"
cargo build --release --jobs %JOBS%
set "BUILD_ERR=%ERRORLEVEL%"
popd
if not "%BUILD_ERR%"=="0" (
  echo [x] Build failed.
  goto :fail
)
if not exist "%EXE%" (
  echo [x] Build finished but %EXE% is missing.
  goto :fail
)

if not exist "%DIST%" mkdir "%DIST%"
copy /y "%EXE%" "%DIST%\%APPNAME%.exe" >nul
echo       portable exe: "%DIST%\%APPNAME%.exe"

if /i "%~1"=="install" goto :direct_install

echo [2/3] Looking for Inno Setup...
set "ISCC="
for %%p in ("%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" "%ProgramFiles%\Inno Setup 6\ISCC.exe" "%LocalAppData%\Programs\Inno Setup 6\ISCC.exe") do (
  if not defined ISCC if exist "%%~p" set "ISCC=%%~p"
)
if not defined ISCC for /f "delims=" %%p in ('where iscc 2^>nul') do if not defined ISCC set "ISCC=%%p"
if not defined ISCC (
  echo [!] Inno Setup 6 not found, so no setup file was made.
  echo     Install it from https://jrsoftware.org/isdl.php and run this again,
  echo     or run:  build-installer.bat install   to install straight into Program Files.
  goto :done
)

echo [3/3] Creating installer...
"%ISCC%" /Q "/DAppVersion=%VERSION%" "/DSourceExe=%EXE%" "/DOutputDir=%DIST%" "%ROOT%installer\mkv-batch.iss"
if errorlevel 1 (
  echo [x] Inno Setup failed.
  goto :fail
)
echo.
echo Done. Installer: "%DIST%\MKV-Batch-%VERSION%-setup.exe"
echo It installs to "C:\Program Files\%APPNAME%" with a Start menu entry and uninstaller.
goto :done

:direct_install
echo [2/2] Installing into "%ProgramFiles%\%APPNAME%" (administrator rights needed)...
set "PS1=%TEMP%\mkvbatch-install.ps1"
> "%PS1%"  echo $ErrorActionPreference = 'Stop'
>> "%PS1%" echo $dir = Join-Path $env:ProgramFiles '%APPNAME%'
>> "%PS1%" echo New-Item -ItemType Directory -Force -Path $dir ^| Out-Null
>> "%PS1%" echo Get-Process -Name 'MKV Batch' -ErrorAction SilentlyContinue ^| Stop-Process -Force
>> "%PS1%" echo Copy-Item -Force '%EXE%' (Join-Path $dir '%APPNAME%.exe')
>> "%PS1%" echo Copy-Item -Force '%ROOT%installer\mkv-batch.ico' (Join-Path $dir 'mkv-batch.ico')
>> "%PS1%" echo $shell = New-Object -ComObject WScript.Shell
>> "%PS1%" echo $lnk = $shell.CreateShortcut((Join-Path $env:ProgramData 'Microsoft\Windows\Start Menu\Programs\%APPNAME%.lnk'))
>> "%PS1%" echo $lnk.TargetPath = (Join-Path $dir '%APPNAME%.exe')
>> "%PS1%" echo $lnk.WorkingDirectory = $dir
>> "%PS1%" echo $lnk.Save()
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -Wait -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"%PS1%\"'"
del "%PS1%" >nul 2>nul
if exist "%ProgramFiles%\%APPNAME%\%APPNAME%.exe" (
  echo Installed: "%ProgramFiles%\%APPNAME%\%APPNAME%.exe"  ^(Start menu: %APPNAME%^)
) else (
  echo [x] Install was cancelled or failed.
  goto :fail
)

:done
echo.
pause
exit /b 0

:fail
echo.
pause
exit /b 1
