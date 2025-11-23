#!/usr/bin/env python3
"""
Screenshot Analysis - Report what's visible in captured images
"""
from PIL import Image
import os

def analyze_screenshot(filename):
    """Analyze a screenshot and report basic info"""
    if not os.path.exists(filename):
        return f"[MISSING] {filename} not found"
    
    try:
        img = Image.open(filename)
        width, height = img.size
        mode = img.mode
        
        # Calculate if image appears mostly dark or light
        # Sample pixels to estimate brightness
        pixels = list(img.getdata())
        if mode == 'RGB':
            avg_brightness = sum(sum(p) for p in pixels[:1000]) / (len(pixels[:1000]) * 3)
        elif mode == 'RGBA':
            avg_brightness = sum(sum(p[:3]) for p in pixels[:1000]) / (len(pixels[:1000]) * 3)
        else:
            avg_brightness = 0
        
        brightness_desc = "BRIGHT" if avg_brightness > 128 else "DARK"
        
        return f"""
[OK] {filename}
     Size: {width}x{height} pixels
     Mode: {mode}
     Brightness: {brightness_desc} (avg: {avg_brightness:.1f}/255)
     File size: {os.path.getsize(filename):,} bytes
"""
    except Exception as e:
        return f"[ERROR] {filename}: {e}"

def main():
    print("="*60)
    print("SCREENSHOT ANALYSIS")
    print("="*60)
    
    screenshots = [
        'td_verification.png',
        'firefox_verification.png', 
        'obs_verification.png',
        'screenshot_test.png'
    ]
    
    for screenshot in screenshots:
        print(analyze_screenshot(screenshot))
    
    print("="*60)
    print("\nNOTE: To visually verify the pipeline:")
    print("1. Open td_verification.png to see TouchDesigner")
    print("2. Look for webrender_livekit_input operator")
    print("3. Check if video is visible in the operator")
    print("\nIf video is visible in TouchDesigner webrender:")
    print("  => PIPELINE 100% COMPLETE!")

if __name__ == "__main__":
    main()
