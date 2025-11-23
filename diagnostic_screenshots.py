import pyautogui
import time
from PIL import ImageGrab

print("Taking before screenshot...")
before = ImageGrab.grab()
before.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/before.png')

print("Clicking TD window...")
pyautogui.moveTo(1720, 684)
pyautogui.click()
time.sleep(1)

print("Taking after-click screenshot...")
after_click = ImageGrab.grab()
after_click.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/after_click.png')

print("Sending Alt+T...")
pyautogui.hotkey('alt', 't')
time.sleep(1.5)

print("Taking after-alt-t screenshot...")
after_altt = ImageGrab.grab()
after_altt.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/after_altt.png')

print("Typing 'test'...")
pyautogui.typewrite('test')
time.sleep(0.5)

print("Taking after-test screenshot...")
after_test = ImageGrab.grab()
after_test.save('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/after_test.png')

print("\n" + "="*60)
print("Screenshots saved! Check them to see what's happening")
print("="*60)
