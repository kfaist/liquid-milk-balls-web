# Load LiveKit Cloud Publisher in TouchDesigner
wr1 = op('/project1/webrender1')
wr1.par.url = 'http://localhost:3000/livekit_cloud_publisher.html'
wr1.par.reloadsrc.pulse()
print("="*60)
print("LOADED: LiveKit Cloud Publisher")
print("="*60)
print("Watch the WebRender output for status messages")
print("Should show:")
print("  1. Camera captured")
print("  2. Token received")
print("  3. Connected to LiveKit Cloud")
print("  4. Camera published")
print("="*60)
