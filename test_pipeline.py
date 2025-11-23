"""
Complete Pipeline Test Script
Tests all components of the video processing loop
"""
import requests
import time

def test_server():
    """Test if local server is running"""
    try:
        response = requests.get("http://localhost:3000/healthz", timeout=2)
        if response.status_code == 200:
            print("[OK] Server is running on port 3000")
            return True
        else:
            print(f"[FAIL] Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Server not responding: {e}")
        return False

def test_publisher_page():
    """Test if publisher page is accessible"""
    try:
        response = requests.get("http://localhost:3000/publisher.html", timeout=2)
        if response.status_code == 200:
            print("[OK] Publisher page is accessible")
            return True
        else:
            print(f"[FAIL] Publisher page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Publisher page error: {e}")
        return False

def test_viewer_page():
    """Test if return viewer page is accessible"""
    try:
        response = requests.get("http://localhost:3000/return-viewer.html", timeout=2)
        if response.status_code == 200:
            print("[OK] Return viewer page is accessible")
            return True
        else:
            print(f"[FAIL] Return viewer page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Return viewer page error: {e}")
        return False

def test_token_api():
    """Test if LiveKit token generation works"""
    try:
        response = requests.get("http://localhost:3000/api/processed-publisher-token", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if 'token' in data and 'whipUrl' in data:
                print(f"[OK] Token API working")
                print(f"     WHIP URL: {data['whipUrl'][:80]}...")
                return True
            else:
                print(f"[FAIL] Token API missing fields: {data.keys()}")
                return False
        else:
            print(f"[FAIL] Token API returned {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Token API error: {e}")
        return False

def main():
    print("="*60)
    print("PIPELINE HEALTH CHECK")
    print("="*60)
    
    results = {
        "Server": test_server(),
        "Publisher Page": test_publisher_page(),
        "Viewer Page": test_viewer_page(),
        "Token API": test_token_api()
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for component, status in results.items():
        symbol = "[OK]" if status else "[FAIL]"
        print(f"{symbol} {component}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("ALL SYSTEMS OPERATIONAL!")
        print("="*60)
        print("\nNext steps:")
        print("1. Open OBS")
        print("2. Enable WebSocket Server:")
        print("   - Tools > WebSocket Server Settings")
        print("   - [X] Enable WebSocket server")
        print("   - Leave password blank")
        print("   - Click OK")
        print("3. Click 'Start Streaming'")
        print("4. Open http://localhost:3000/publisher.html")
        print("5. Open http://localhost:3000/return-viewer.html")
    else:
        print("SOME SYSTEMS FAILED - Check errors above")
        print("="*60)

if __name__ == "__main__":
    main()
