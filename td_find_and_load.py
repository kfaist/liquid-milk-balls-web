# Find all webrender operators in your TouchDesigner project

print("="*60)
print("🔍 SEARCHING FOR WEBRENDER OPERATORS...")
print("="*60)

# Search the entire project for webrender operators
webrender_ops = root.findChildren(type=TOP, name='webrender*')

if len(webrender_ops) == 0:
    print("❌ NO WEBRENDER OPERATORS FOUND!")
    print("")
    print("You need to create one:")
    print("  1. Right-click in network")
    print("  2. Add Operator > TOP > Web Render")
    print("  3. Name it 'webrender1' or 'webrender_livekit'")
    print("")
    print("THEN RUN THIS SCRIPT AGAIN!")
else:
    print(f"✅ FOUND {len(webrender_ops)} WEBRENDER OPERATOR(S):")
    print("")
    for i, op_found in enumerate(webrender_ops, 1):
        print(f"{i}. {op_found.path}")
        print(f"   Current URL: {op_found.par.url}")
        print("")
    
    # Use the first one found
    if len(webrender_ops) > 0:
        wr = webrender_ops[0]
        print("="*60)
        print("🎯 LOADING LIVEKIT PUBLISHER INTO FIRST WEBRENDER...")
        print("="*60)
        wr.par.url = 'http://localhost:3000/livekit_cloud_publisher.html'
        wr.par.reloadsrc.pulse()
        print("")
        print(f"✅ Loaded into: {wr.path}")
        print("")
        print("WATCH THE WEBRENDER OUTPUT FOR GREEN CHECKMARKS!")
        print("="*60)
