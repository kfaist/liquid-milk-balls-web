@echo off
echo ===================================
echo LIQUID MILK BALLS - WEBRTC SETUP
echo ===================================
echo.
echo Starting Node.js server with LiveKit...
echo.

cd /d "C:\Users\krista-showputer\Desktop\liquid-milk-balls-web"

:: Set environment variables
set LIVEKIT_URL=wss://claymation-transcription-l6e51sws.livekit.cloud
set LIVEKIT_API_KEY=APITw2Yp2Tv3yfg
set LIVEKIT_API_SECRET=eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW
set LIVEKIT_ROOM_NAME=claymation-live
set LIVEKIT_PROCESSED_ROOM=processed-output

echo Environment variables set!
echo.
echo Starting server...
npm start

pause
