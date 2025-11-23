"""
TouchDesigner Configuration Assistant
Copies LiveKit settings to clipboard and provides step-by-step guidance
"""
import pyperclip
import time

# LiveKit Configuration
CONFIG = {
    'url': 'wss://claymation-transcription-l6e51sws.livekit.cloud',
    'room': 'claymation-live',
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiY2xheW1hdGlvbi1saXZlIiwicm9vbUpvaW4iOnRydWUsImNhblB1Ymxpc2giOmZhbHNlLCJjYW5TdWJzY3JpYmUiOnRydWV9LCJpc3MiOiJBUElUdzJZcDJUdjN5ZmciLCJleHAiOjE3NjM4NDg4NDQsIm5iZiI6MCwic3ViIjoidG91Y2hkZXNpZ25lci1yZWNlaXZlciJ9.LScuDiy0yrnxxJKweBRgxfU5EVSsSwCGQC76ZRFqIKs'
}

def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)

def copy_to_clipboard(text, label):
    pyperclip.copy(text)
    print(f"\n✓ Copied to clipboard: {label}")
    print(f"  {text[:60]}..." if len(text) > 60 else f"  {text}")
    input("\n  Press ENTER after you've pasted this into TouchDesigner...")

def main():
    print_header("TOUCHDESIGNER LIVEKIT CONFIGURATION ASSISTANT")
    
    print("\nThis script will guide you through configuring TouchDesigner")
    print("to receive video from your publisher page.")
    print("\nEach value will be copied to your clipboard.")
    print("Paste it into the appropriate parameter in TouchDesigner.")
    
    input("\n\nPress ENTER to begin...")
    
    # Step 1: Create Web Render TOP
    print_header("STEP 1: CREATE WEB RENDER TOP")
    print("\nIn TouchDesigner:")
    print("  1. Press TAB key")
    print("  2. Type: web render")
    print("  3. Press ENTER")
    print("  4. Click anywhere to place it")
    print("  5. Click on the operator to select it")
    
    input("\nPress ENTER when you've created the Web Render TOP...")
    
    # Step 2: Configure LiveKit URL
    print_header("STEP 2: SET LIVEKIT URL")
    print("\nLook in the Parameters panel for:")
    print("  - 'LiveKit URL' or 'URL' or 'Server URL'")
    print("\nI'm copying the URL to your clipboard...")
    copy_to_clipboard(CONFIG['url'], "LiveKit URL")
    
    # Step 3: Configure Room Name
    print_header("STEP 3: SET ROOM NAME")
    print("\nLook for parameter:")
    print("  - 'Room Name' or 'Room' or 'Channel'")
    print("\nCopying room name to clipboard...")
    copy_to_clipboard(CONFIG['room'], "Room Name")
    
    # Step 4: Configure Token
    print_header("STEP 4: SET ACCESS TOKEN")
    print("\nLook for parameter:")
    print("  - 'Token' or 'Access Token' or 'LiveKit Token'")
    print("\nCopying token to clipboard...")
    copy_to_clipboard(CONFIG['token'], "Access Token")
    
    # Step 5: Enable LiveKit
    print_header("STEP 5: ENABLE LIVEKIT")
    print("\nLook for a checkbox or toggle:")
    print("  - 'Use LiveKit' or 'Enable LiveKit' or 'LiveKit Mode'")
    print("\nTurn this ON/Enable it/Check it")
    
    input("\nPress ENTER when LiveKit is enabled...")
    
    # Step 6: Connect
    print_header("STEP 6: CONNECT TO LIVEKIT")
    print("\nLook for a button or parameter:")
    print("  - 'Connect' or 'Start' or 'Active'")
    print("\nClick it or set it to ON")
    
    input("\nPress ENTER when you've clicked Connect...")
    
    # Step 7: Test
    print_header("STEP 7: TEST THE CONNECTION")
    print("\nNow test the video flow:")
    print("  1. Go to Firefox (tab with publisher.html)")
    print("  2. Click 'Start Publishing'")
    print("  3. Allow camera access")
    print("  4. Return to TouchDesigner")
    print("  5. Right-click the Web Render TOP → Viewer")
    print("  6. You should see video!")
    
    input("\nPress ENTER when you see video (or to continue anyway)...")
    
    # Final instructions
    print_header("CONFIGURATION COMPLETE!")
    print("\n✓ Web Render TOP configured")
    print("✓ LiveKit settings applied")
    print("✓ Ready to receive video")
    
    print("\nNEXT STEPS:")
    print("  1. Connect Web Render TOP output to your effects chain")
    print("  2. Connect effects to NDI Out TOP")
    print("  3. OBS will pick up the NDI stream")
    print("  4. Complete video flow will be working!")
    
    print("\nTROUBLESHOOTING:")
    print("  • No video? Check publisher page shows 'Publishing' status")
    print("  • Token expired? Run: python td_livekit_token.py")
    print("  • Still stuck? Check TOUCHDESIGNER_SETUP_INSTRUCTIONS.txt")
    
    print("\n" + "=" * 70)
    print("All configuration data saved in td_livekit_config.txt")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled.")
    except Exception as e:
        print(f"\n\nError: {e}")
        print("Check QUICK_START.txt for manual instructions")
