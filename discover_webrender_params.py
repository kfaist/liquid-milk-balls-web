"""
Discover WebRender TOP parameters in TouchDesigner
"""
import pyautogui
import time

def execute_td_command(command):
    """Execute a command in TouchDesigner textport"""
    pyautogui.write(command, interval=0.01)
    pyautogui.press('enter')
    time.sleep(0.5)

def main():
    print("Discovering WebRender TOP parameters...")
    
    # Focus TouchDesigner and open textport
    pyautogui.hotkey('alt', 't')
    time.sleep(1)
    
    # Clear textport
    execute_td_command("import sys; sys.stdout.flush()")
    
    # Get the WebRender TOP
    execute_td_command("wr = op('/webrender_livekit_input')")
    execute_td_command("print('=' * 60)")
    execute_td_command("print('WEBRENDER TOP FOUND:', wr)")
    execute_td_command("print('=' * 60)")
    
    # List all parameters
    execute_td_command("print('\\nALL PARAMETERS:')")
    execute_td_command("for p in wr.pars(): print(f'  {p.name}: {p.val}')")
    
    # Check specific media-related parameters
    execute_td_command("print('\\nMEDIA-RELATED PARAMETERS:')")
    execute_td_command("media_params = [p for p in wr.pars() if 'media' in p.name.lower() or 'enable' in p.name.lower()]")
    execute_td_command("for p in media_params: print(f'  {p.name}: {p.val} (mode: {p.mode.name})')")
    
    # Check URL
    execute_td_command("print('\\nCURRENT URL:')")
    execute_td_command("url_params = [p for p in wr.pars() if 'url' in p.name.lower()]")
    execute_td_command("for p in url_params: print(f'  {p.name}: {p.val}')")
    
    print("\nParameter discovery complete. Check TouchDesigner textport for results.")

if __name__ == "__main__":
    main()
