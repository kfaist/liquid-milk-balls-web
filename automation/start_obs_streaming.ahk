; AutoHotkey Script to Start OBS Streaming
; This script waits for OBS to be running, then clicks "Start Streaming"

#Persistent
#SingleInstance Force

; Wait for OBS to be running
Loop
{
    Process, Exist, obs64.exe
    if (ErrorLevel)
    {
        ; OBS is running, wait 3 seconds for it to fully load
        Sleep, 3000
        break
    }
    ; Check every second
    Sleep, 1000
}

; Activate OBS window
WinActivate, ahk_exe obs64.exe
Sleep, 500

; Send the keyboard shortcut to start streaming
; By default OBS has no hotkey for Start Streaming
; So we'll use the menu: Controls -> Start Streaming
; Or we can use Alt+C (Controls menu) then S (Start Streaming)

; Method 1: Try keyboard navigation
Send, !c
Sleep, 200
Send, s
Sleep, 200

; Alternative Method 2: If keyboard doesn't work, use mouse click
; Uncomment these lines and adjust coordinates if needed
; WinGetPos, X, Y, Width, Height, ahk_exe obs64.exe
; Click at approximate position of Start Streaming button
; Click, % Width - 100, % Height - 50

ExitApp
