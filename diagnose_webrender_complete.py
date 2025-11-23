"""
Complete diagnostic and fix for TouchDesigner WebRender TOP
This script will:
1. Take screenshots of current TouchDesigner state
2. Check if WebRender TOP exists and its current configuration
3. Enable "Enable Media Stream" if not already enabled
4. Set correct URL (http://localhost:3000/td-auto-viewer.html)
5. Reload the WebRender TOP
6. Verify the configuration
"""

import pyautogui
import time
import subprocess
from PIL import Image
import os

# Ensure TouchDesigner window is focused
def focus_touchdesigner():
    """Focus the TouchDesigner window"""
    print("Focusing TouchDesigner window...")
    try:
        # Find TouchDesigner window
        subprocess.run([
            "powershell", 
            "-Command",
            "$win = Get-Process -Name 'TouchDesigner' -ErrorAction SilentlyContinue | Select-Object -First 1; " +
            "if ($win) { " +
            "    Add-Type @\\\"" +
            "        using System;" +
            "        using System.Runtime.InteropServices;" +
            "        public class Win32 {" +
            "            [DllImport(\\\"user32.dll\\\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);" +
            "            [DllImport(\\\"user32.dll\\\")] public static extern bool SetForegroundWindow(IntPtr hWnd);" +
            "        }" +
            "    \\\"@;" +
            "    $h = $win.MainWindowHandle;" +
            "    [Win32]::ShowWindow($h, 9);" +
            "    [Win32]::SetForegroundWindow($h);" +
            "}"
        ], check=True)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error focusing TouchDesigner: {e}")
        return False

def take_screenshot(filename):
    """Take a screenshot of the current screen"""
    print(f"Taking screenshot: {filename}")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
    return filename

def main():
    print("=" * 70)
    print("TOUCHDESIGNER WEBRENDER TOP DIAGNOSTIC AND FIX")
    print("=" * 70)
    
    # Step 1: Take initial screenshot
    focus_touchdesigner()
    take_screenshot("td_initial_diagnostic.png")
    
    print("\n" + "=" * 70)
    print("STEP 1: Initial screenshot captured")
    print("=" * 70)
    
    # Step 2: Open the textport to execute commands
    print("\nOpening TextPort to execute commands...")
    print("Pressing Alt+T to open TextPort...")
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Step 3: Check if WebRender TOP exists
    print("\nChecking for WebRender TOP...")
    command = "print(op('/webrender_livekit_input'))"
    pyautogui.write(command, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Take screenshot of textport output
    take_screenshot("td_webrender_check.png")
    
    # Step 4: Check current parameters
    print("\nChecking WebRender TOP parameters...")
    check_commands = [
        "wr = op('/webrender_livekit_input')",
        "print('Enablemediastream:', wr.par.Enablemediastream if hasattr(wr.par, 'Enablemediastream') else 'N/A')",
        "print('URL:', wr.par.Url if hasattr(wr.par, 'Url') else 'N/A')",
        "print('Enablemedia:', wr.par.Enablemedia if hasattr(wr.par, 'Enablemedia') else 'N/A')",
        "print('Enableaudio:', wr.par.Enableaudio if hasattr(wr.par, 'Enableaudio') else 'N/A')",
    ]
    
    for cmd in check_commands:
        pyautogui.write(cmd, interval=0.01)
        pyautogui.press('enter')
        time.sleep(0.3)
    
    time.sleep(1)
    take_screenshot("td_webrender_params_before.png")
    
    # Step 5: Configure WebRender TOP properly
    print("\nConfiguring WebRender TOP with correct settings...")
    config_commands = [
        "wr = op('/webrender_livekit_input')",
        "wr.par.Url = 'http://localhost:3000/td-auto-viewer.html'",
        "# Try different parameter names for Enable Media Stream",
        "if hasattr(wr.par, 'Enablemediastream'): wr.par.Enablemediastream = True",
        "if hasattr(wr.par, 'Enablemedia'): wr.par.Enablemedia = True", 
        "if hasattr(wr.par, 'Enableaudio'): wr.par.Enableaudio = True",
        "print('WebRender TOP configured successfully')",
        "print('URL:', wr.par.Url)",
    ]
    
    for cmd in config_commands:
        pyautogui.write(cmd, interval=0.01)
        pyautogui.press('enter')
        time.sleep(0.3)
    
    time.sleep(1)
    take_screenshot("td_webrender_configured.png")
    
    # Step 6: Reload the WebRender TOP
    print("\nReloading WebRender TOP...")
    reload_commands = [
        "wr = op('/webrender_livekit_input')",
        "# Pulse the Reload parameter",
        "if hasattr(wr.par, 'Reload'): wr.par.Reload.pulse()",
        "print('WebRender TOP reloaded')",
    ]
    
    for cmd in reload_commands:
        pyautogui.write(cmd, interval=0.01)
        pyautogui.press('enter')
        time.sleep(0.3)
    
    time.sleep(2)  # Wait for reload
    take_screenshot("td_webrender_after_reload.png")
    
    # Step 7: Verify the configuration
    print("\nVerifying final configuration...")
    verify_commands = [
        "wr = op('/webrender_livekit_input')",
        "print('=' * 50)",
        "print('FINAL WEBRENDER TOP CONFIGURATION:')",
        "print('=' * 50)",
        "print('URL:', wr.par.Url.eval())",
        "if hasattr(wr.par, 'Enablemediastream'): print('Enablemediastream:', wr.par.Enablemediastream.eval())",
        "if hasattr(wr.par, 'Enablemedia'): print('Enablemedia:', wr.par.Enablemedia.eval())",
        "if hasattr(wr.par, 'Enableaudio'): print('Enableaudio:', wr.par.Enableaudio.eval())",
        "print('Width:', wr.width)",
        "print('Height:', wr.height)",
        "print('=' * 50)",
    ]
    
    for cmd in verify_commands:
        pyautogui.write(cmd, interval=0.01)
        pyautogui.press('enter')
        time.sleep(0.3)
    
    time.sleep(1)
    take_screenshot("td_webrender_final_config.png")
    
    # Step 8: Close textport and take final screenshot of network
    print("\nClosing TextPort...")
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    take_screenshot("td_final_network_view.png")
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)
    print("\nScreenshots saved:")
    print("1. td_initial_diagnostic.png - Initial state")
    print("2. td_webrender_check.png - WebRender existence check")
    print("3. td_webrender_params_before.png - Parameters before configuration")
    print("4. td_webrender_configured.png - After configuration")
    print("5. td_webrender_after_reload.png - After reload")
    print("6. td_webrender_final_config.png - Final configuration")
    print("7. td_final_network_view.png - Final network view")
    print("\nNEXT STEPS:")
    print("1. Open a browser to http://localhost:3000/publisher.html")
    print("2. Click 'Start Publishing' to send camera to LiveKit")
    print("3. Check if WebRender TOP in TouchDesigner shows video")
    print("=" * 70)

if __name__ == "__main__":
    main()
