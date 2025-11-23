# WHEN YOU GET BACK - RUN THIS IN TOUCHDESIGNER TEXTPORT
# This reloads everything fresh!

print("="*60)
print("🎯 WELCOME BACK! Loading LiveKit Publisher...")
print("="*60)

wr1 = op('/project1/webrender1')
wr1.par.url = 'http://localhost:3000/livekit_cloud_publisher.html'
wr1.par.reloadsrc.pulse()

print("")
print("✅ Publisher loaded!")
print("")
print("WATCH THE WEBRENDER OUTPUT FOR:")
print("  ✓ LiveKit library loaded")
print("  ✓ Camera captured")
print("  ✓ Token received")
print("  ✓ Connected to LiveKit Cloud")
print("  ✓ Camera published")
print("")
print("="*60)
print("IF YOU SEE ALL GREEN CHECKMARKS = WE DID IT!")
print("="*60)
