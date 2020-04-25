@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=pretzel_logic
set NAME=PretzelLogic
set PACKID=1168065472
set VERSION=0.1.1


echo %VERSION% >%REPO%\VERSION

fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%\checksum.md5

%ZIP% %NAME%_v%VERSION%_Anki20.zip *.py %REPO%\*

cd %REPO%

quick_manifest.exe "Pretzel Logic: Retention Benchmarking" "%PACKID%" >manifest.json
%ZIP% ../%NAME%_v%VERSION%_Anki21.ankiaddon *

quick_manifest.exe "Pretzel Logic: Retention Benchmarking" "%REPO%" >manifest.json
%ZIP% ../%NAME%_v%VERSION%_CCBC.adze *
