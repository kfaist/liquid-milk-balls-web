# AUTO-CONFIGURE WEB CLIENT TOP FOR TD-INPUT-VIEWER
import sys

print("=" * 80)
print("🔧 AUTO-CONFIGURING WEB CLIENT TOP FOR LIVEKIT INPUT")
print("=" * 80)

# Find existing Web Client TOP or create one
web_clients = root.findChildren(type='webclientTOP')

if web_clients:
    web = web_clients[0]
    print(f"\n✅ Using existing Web Client TOP: {web.path}")
else:
    # Create a new one at root level
    web = root.create('webclientTOP', 'livekit_input_viewer')
    print(f"\n✅ Created new Web Client TOP: {web.path}")

print("\n🔧 Configuring parameters...")

# Set URL to our td-input-viewer.html
web.par.url = "http://localhost:3000/td-input-viewer.html"
print(f"  ✅ URL: {web.par.url.eval()}")

# Set resolution
web.par.resolutionw = 1920
web.par.resolutionh = 1080
print(f"  ✅ Resolution: {web.par.resolutionw.eval()} x {web.par.resolutionh.eval()}")

# Enable audio
web.par.audio = 'on'
print(f"  ✅ Audio: {web.par.audio.eval()}")

# Make sure it's active
web.par.active = True
print(f"  ✅ Active: {web.par.active.eval()}")

# Force reload
print("\n🔄 Forcing page reload...")
web.par.reload.pulse()
print("  ✅ Reload triggered!")

print("\n" + "=" * 80)
print("✅ CONFIGURATION COMPLETE!")
print("=" * 80)
print("\nThe Web Client TOP should now be displaying the LiveKit input stream.")
print("Make sure you have a publisher connected at http://localhost:3000/publisher.html")
print("\n💡 TIP: Open the publisher in Firefox and allow camera access!")
