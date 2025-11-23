"""
Capture TouchDesigner textport output and configure WebRender TOP
"""
import pyautogui
import time

def take_screenshot(filename):
    """Take and save screenshot"""
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")

def main():
    print("Capturing TouchDesigner textport...")
    
    # Focus TouchDesigner
    pyautogui.click(500, 500)  # Click on screen to ensure focus
    time.sleep(1)
    
    # Open textport if not already open
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Take screenshot of textport
    take_screenshot("td_textport_params.png")
    
    print("\nNow configuring WebRender TOP with correct settings...")
    
    # Configure the WebRender TOP
    commands = [
        "# Get the WebRender TOP",
        "wr = op('/webrender_livekit_input')",
        "",
        "# Set URL to LiveKit viewer page",
        "wr.par.Url = 'http://localhost:3000/td-auto-viewer.html'",
        "",
        "# Enable media stream - try all possible parameter names",
        "if hasattr(wr.par, 'Enablemediastream'): wr.par.Enablemediastream = 1",
        "if hasattr(wr.par, 'Enablemedia'): wr.par.Enablemedia = 1",
        "if hasattr(wr.par, 'Enableaudio'): wr.par.Enableaudio = 1",
        "",
        "# Reload the page",
        "if hasattr(wr.par, 'Reload'): wr.par.Reload.pulse()",
        "",
        "print('=' * 60)",
        "print('WEBRENDER TOP CONFIGURED!')",
        "print('=' * 60)",
        "print('URL:', wr.par.Url.eval())",
        "print('Now test by opening http://localhost:3000/publisher.html')",
        "print('=' * 60)",
    ]
    
    for cmd in commands:
        if cmd.strip():  # Skip empty lines
            pyautogui.write(cmd, interval=0.01)
            pyautogui.press('enter')
            time.sleep(0.3)
    
    time.sleep(2)
    
    # Take screenshot after configuration
    take_screenshot("td_webrender_configured_final.png")
    
    # Close textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Take screenshot of network view
    take_screenshot("td_network_configured.png")
    
    print("\n" + "=" * 60)
    print("CONFIGURATION COMPLETE!")
    print("=" * 60)
    print("\nScreenshots saved:")
    print("1. td_textport_params.png - Parameter discovery results")
    print("2. td_webrender_configured_final.png - After configuration")
    print("3. td_network_configured.png - Final network view")
    print("\nNEXT STEP: Test the WebRender TOP")
    print("Open http://localhost:3000/publisher.html in browser")
    print("Click 'Start Publishing' to send camera to LiveKit")
    print("=" * 60)

if __name__ == "__main__":
    main()
