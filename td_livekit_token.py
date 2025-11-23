"""
TouchDesigner LiveKit Token Generator
Run this to get a token for TD to receive video from the publisher
"""
import requests
import json

# Your Railway app URL
RAILWAY_URL = "https://liquid-milk-balls-web-production-2e8c.up.railway.app"

def get_td_viewer_token():
    """Get a viewer token for TouchDesigner to subscribe to the input room"""
    try:
        # Request a viewer token for the input room (claymation-live)
        response = requests.get(f"{RAILWAY_URL}/api/viewer-token?identity=touchdesigner-receiver")
        
        if response.status_code == 200:
            data = response.json()
            print("\n" + "="*60)
            print("TOUCHDESIGNER LIVEKIT CONNECTION INFO")
            print("="*60)
            print(f"\nLiveKit URL: {data['url']}")
            print(f"Room Name: {data['room']}")
            print(f"\nToken (copy this):\n{data['token']}")
            print("\n" + "="*60)
            print("\nSTEPS TO CONFIGURE TOUCHDESIGNER:")
            print("1. Open your ndi-streamCOPY.toe project")
            print("2. Find or create a 'Web Render TOP' operator")
            print("3. In the Web Render TOP parameters:")
            print("   - Enable 'Use LiveKit'")
            print("   - Set 'LiveKit URL' to:", data['url'])
            print("   - Set 'LiveKit Token' to the token above")
            print("   - Set 'Room Name' to:", data['room'])
            print("4. Click 'Connect' or activate the operator")
            print("5. Video from publisher.html should appear!")
            print("="*60 + "\n")
            
            # Save to file for easy access
            with open("td_livekit_config.txt", "w") as f:
                f.write(f"LiveKit URL: {data['url']}\n")
                f.write(f"Room Name: {data['room']}\n")
                f.write(f"Token: {data['token']}\n")
            print("✓ Configuration saved to td_livekit_config.txt")
            
            return data
        else:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("\nFetching LiveKit token for TouchDesigner...")
    get_td_viewer_token()
