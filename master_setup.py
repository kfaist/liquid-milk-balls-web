# MASTER SETUP SCRIPT FOR TOUCHDESIGNER LIVEKIT INPUT
# This script will fully configure a Web Client TOP to receive LiveKit video

import sys

print("=" * 80)
print("🚀 TOUCHDESIGNER LIVEKIT INPUT - MASTER SETUP")
print("=" * 80)

# Step 1: Find or create Web Client TOP
print("\n📍 STEP 1: Locating Web Client TOP...")

web_clients = root.findChildren(type='webclientTOP')

if len(web_clients) == 0:
    print("  ⚠️  No Web Client TOP found. Creating new one...")
    web = root.create('webclientTOP', 'livekit_input')
    print(f"  ✅ Created: {web.path}")
else:
    # Use the first one found
    web = web_clients[0]
    print(f"  ✅ Found existing: {web.path}")
    
    # List all if multiple
    if len(web_clients) > 1:
        print(f"  ℹ️  Note: Found {len(web_clients)} Web Client TOPs:")
        for i, w in enumerate(web_clients, 1):
            print(f"     {i}. {w.path}")
        print("     Using the first one.")

# Step 2: Configure parameters
print("\n🔧 STEP 2: Configuring parameters...")

# URL
TARGET_URL = "http://localhost:3000/td-input-viewer.html"
web.par.url = TARGET_URL
print(f"  ✅ URL: {TARGET_URL}")

# Resolution
web.par.resolutionw = 1920
web.par.resolutionh = 1080
print(f"  ✅ Resolution: 1920 x 1080")

# Audio
web.par.audio = 'on'
print(f"  ✅ Audio: ON")

# Active
web.par.active = True
print(f"  ✅ Active: TRUE")

# Step 3: Reload page
print("\n🔄 STEP 3: Reloading page...")
web.par.reload.pulse()
print("  ✅ Page reload triggered")

# Step 4: Verify configuration
print("\n✅ STEP 4: Verification...")
print(f"  Web Client TOP: {web.path}")
print(f"  URL: {web.par.url.eval()}")
print(f"  Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")
print(f"  Audio: {web.par.audio.eval()}")
print(f"  Active: {web.par.active.eval()}")

# Step 5: Instructions
print("\n" + "=" * 80)
print("✅ CONFIGURATION COMPLETE!")
print("=" * 80)
print("\n📋 WHAT TO DO NEXT:")
print("\n1. Open Firefox and go to:")
print("   http://localhost:3000/publisher.html")
print("\n2. Click 'Allow' when asked for camera permission")
print("\n3. Click 'Start Publishing'")
print("\n4. Look at your Web Client TOP - you should see video!")
print("\n" + "=" * 80)
print("\n💡 TROUBLESHOOTING:")
print("\n   • If you don't see video:")
print("     - Check that publisher is connected (should say 'Publishing' in browser)")
print("     - Try clicking the Reload parameter on the Web Client TOP again")
print("     - Check browser console (F12) for errors")
print("\n   • Test the connection:")
print("     - Open http://localhost:3000/livekit-test.html")
print("     - Click 'CONNECT AS VIEWER'")
print("     - Should show 'Connected' and list participants")
print("\n" + "=" * 80)

print("\n✨ Setup complete! Check the Web Client TOP now! ✨\n")
