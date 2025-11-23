# Script to check all Web Client TOP configurations in TouchDesigner
import sys

print("=" * 80)
print("🔍 CHECKING ALL WEB CLIENT TOP OPERATORS")
print("=" * 80)

# Find all Web Client TOP operators
web_clients = root.findChildren(type='webclientTOP')

if not web_clients:
    print("❌ No Web Client TOP operators found!")
    sys.exit(1)

print(f"\n✅ Found {len(web_clients)} Web Client TOP operator(s):\n")

for i, web in enumerate(web_clients, 1):
    print(f"--- Web Client TOP #{i}: {web.path} ---")
    print(f"  Name: {web.name}")
    
    # Check critical parameters
    try:
        url = web.par.url.eval()
        print(f"  URL: {url}")
    except:
        print("  URL: [ERROR READING]")
    
    try:
        w = web.par.resolutionw.eval()
        h = web.par.resolutionh.eval()
        print(f"  Resolution: {w} x {h}")
    except:
        print("  Resolution: [ERROR READING]")
    
    try:
        audio = web.par.audio.eval()
        print(f"  Audio: {audio}")
    except:
        print("  Audio: [ERROR READING]")
    
    try:
        active = web.par.active.eval()
        print(f"  Active: {active}")
    except:
        print("  Active: [ERROR READING]")
    
    print()

print("=" * 80)
print("✅ CHECK COMPLETE")
print("=" * 80)
