@echo off
echo ============================================================
echo Starting LiveKit Token Endpoint
echo ============================================================

cd /d C:\Users\krista-showputer\Desktop\liquid-milk-balls-web

echo Loading environment variables from .env...
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%a"=="#" (
        set "%%a=%%b"
    )
)

echo.
echo Configuration:
echo   API Key: %LIVEKIT_API_KEY%
echo   LiveKit URL: %LIVEKIT_URL%
echo   Room: %LIVEKIT_ROOM_NAME%
echo.

echo Starting token endpoint on port 3001...
node livekit_token_endpoint.js

pause
