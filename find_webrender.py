"""
Find and display webrender_livekit_input operator in TouchDesigner
"""
import pyautogui
import time

print("="*60)
print("FINDING WEBRENDER_LIVEKIT_INPUT OPERATOR")
print("="*60)

# TouchDesigner should be active
time.sleep(1)

# Try to search for the operator using Ctrl+F or network navigation
print("\n[1/3] Attempting to navigate to webrender operator...")

# Option 1: Use keyboard to navigate
# Press Tab to show operator names
pyautogui.press('tab')
time.sleep(0.5)

# Take screenshot of current view
print("[2/3] Capturing current view...")
screenshot = pyautogui.screenshot()
screenshot.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\touchdesigner_operators.png')
print("[OK] Screenshot saved: touchdesigner_operators.png")

# Try to zoom out to see more of the network
print("[3/3] Zooming out to see full network...")
pyautogui.hotkey('ctrl', '0')  # Reset zoom
time.sleep(0.5)

# Take another screenshot
screenshot2 = pyautogui.screenshot()
screenshot2.save(r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\touchdesigner_network.png')
print("[OK] Screenshot saved: touchdesigner_network.png")

print("\n" + "="*60)
print("Screenshots captured for analysis")
print("="*60)
