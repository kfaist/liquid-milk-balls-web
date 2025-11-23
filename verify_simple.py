#!/usr/bin/env python3
"""
Pipeline Verification Script - Simple Text Version
"""
import pyautogui
import time
import pygetwindow as gw
import subprocess
import sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

def find_window(title_contains):
    """Find window by partial title match"""
    windows = gw.getWindowsWithTitle(title_contains)
    return windows[0] if windows else None

def check_touchdesigner():
    """Check if TouchDesigner is running and visible"""
    print("\n" + "="*60)
    print("CHECKING TOUCHDESIGNER")
    print("="*60)
    
    td_window = find_window('TouchDesigner')
    
    if td_window:
        print(f"[OK] TouchDesigner window found: {td_window.title}")
        print(f"     Position: {td_window.left}, {td_window.top}")
        print(f"     Size: {td_window.width}x{td_window.height}")
        
        try:
            td_window.activate()
            time.sleep(1)
            print("[OK] TouchDesigner brought to front")
            
            screenshot = pyautogui.screenshot()
            screenshot.save('td_verification.png')
            print("[OK] Screenshot saved: td_verification.png")
            
        except Exception as e:
            print(f"[WARN] Could not activate window: {e}")
            
        return True
    else:
        print("[FAIL] TouchDesigner window not found")
        return False

def check_firefox_tabs():
    """Check Firefox tabs"""
    print("\n" + "="*60)
    print("CHECKING FIREFOX TABS")
    print("="*60)
    
    ff_window = find_window('Firefox')
    
    if ff_window:
        print(f"[OK] Firefox window found: {ff_window.title}")
        
        try:
            ff_window.activate()
            time.sleep(1)
            print("[OK] Firefox brought to front")
            
            screenshot = pyautogui.screenshot()
            screenshot.save('firefox_verification.png')
            print("[OK] Screenshot saved: firefox_verification.png")
            
        except Exception as e:
            print(f"[WARN] Could not activate Firefox: {e}")
            
        return True
    else:
        print("[FAIL] Firefox window not found")
        return False

def check_obs():
    """Check OBS Studio"""
    print("\n" + "="*60)
    print("CHECKING OBS STUDIO")
    print("="*60)
    
    obs_window = find_window('OBS')
    
    if obs_window:
        print(f"[OK] OBS window found: {obs_window.title}")
        
        try:
            obs_window.activate()
            time.sleep(1)
            print("[OK] OBS brought to front")
            
            screenshot = pyautogui.screenshot()
            screenshot.save('obs_verification.png')
            print("[OK] Screenshot saved: obs_verification.png")
            
        except Exception as e:
            print(f"[WARN] Could not activate OBS: {e}")
            
        return True
    else:
        print("[INFO] OBS window not found")
        return False

def check_node_server():
    """Check if Node server is running"""
    print("\n" + "="*60)
    print("CHECKING NODE SERVER")
    print("="*60)
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Process -Id 43492 -ErrorAction SilentlyContinue'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("[OK] Node server running (PID 43492)")
            return True
        else:
            print("[FAIL] Node server not found (PID 43492)")
            return False
    except Exception as e:
        print(f"[WARN] Error checking Node server: {e}")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("TOUCHDESIGNER WEBRTC PIPELINE VERIFICATION")
    print("="*60)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'node': check_node_server(),
        'touchdesigner': check_touchdesigner(),
        'firefox': check_firefox_tabs(),
        'obs': check_obs()
    }
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for component, status in results.items():
        status_text = "[OK]" if status else "[FAIL]"
        print(f"{status_text} {component.upper()}: {'RUNNING' if status else 'NOT FOUND'}")
    
    print("\n" + "="*60)
    print("SCREENSHOTS SAVED:")
    print("="*60)
    if results['touchdesigner']:
        print("  td_verification.png - TouchDesigner view")
    if results['firefox']:
        print("  firefox_verification.png - Browser tabs")
    if results['obs']:
        print("  obs_verification.png - OBS Studio")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Review screenshots to verify video is visible")
    print("2. Check TouchDesigner webrender_livekit_input operator")
    print("3. Open Firefox tab 61 and press F12 to check console")
    print("4. Verify camera is streaming in Firefox tab 60")
    
    overall_status = all(results.values())
    if overall_status:
        print("\n[OK] ALL SYSTEMS OPERATIONAL!")
    else:
        print("\n[WARN] Some components not found - check details above")
    
    return overall_status

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
