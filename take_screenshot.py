"""Take screenshot of current screen"""
import pyautogui
import os

output_path = r'C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\screenshot_test.png'

print("Taking screenshot...")
screenshot = pyautogui.screenshot()
screenshot.save(output_path)
print(f"[OK] Screenshot saved to: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
