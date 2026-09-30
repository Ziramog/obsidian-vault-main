@echo off
REM ---------------------------------------------------------------
REM Puerta Hermes PWA (nodo PC). Sin esto, si el proceso muere o la
REM PC se reinicia, el celular de Juan se queda sin puerta.
REM
REM Las DOS variables son obligatorias y su ausencia NO se ve:
REM   HERMES_HOME            sin ella: health 200 con profileCount:0 (0 perfiles locales)
REM   HERMES_PEER_PWA_URL    sin ella: el armado de la cache de ruteo aborta y
REM                          devuelve NODE_UNREACHABLE -> 502 en TODOS los perfiles,
REM                          incluidos los locales de esta misma maquina
REM ---------------------------------------------------------------
set "HERMES_HOME=C:\Users\ingju\AppData\Local\hermes"
set "HERMES_PEER_PWA_URL=http://100.124.132.48:3000"
set "SRC=C:\Projects\hermes-pwa"
set "LOG=C:\Users\ingju\AppData\Local\hermes\logs\puerta-pwa.log"

cd /d "%SRC%" || exit /b 1
if not exist "%SRC%\.next\BUILD_ID" (
  call npm run build >> "%LOG%" 2>&1 || exit /b 1
)

:loop
echo [%DATE% %TIME%] arrancando puerta :3000 >> "%LOG%"
call npx next start -p 3000 -H 0.0.0.0 >> "%LOG%" 2>&1
echo [%DATE% %TIME%] la puerta termino; reintento en 10s >> "%LOG%"
timeout /t 10 /nobreak >nul
goto loop
