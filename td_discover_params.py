# Discover WebRender Parameter Names
print("=" * 60)
print("WEBRENDER PARAMETER DISCOVERY")
print("=" * 60)

paths = ['/project1/webrender1', '/project1/webrender_livekit_input']

for path in paths:
    try:
        wr = op(path)
        if not wr:
            print(f"\n{path} - NOT FOUND")
            continue
            
        print(f"\n[{path}]")
        print(f"Type: {wr.type}")
        print(f"\nALL Parameters:")
        
        for p in wr.pars():
            pname = p.name.lower()
            # Show ALL parameters so we can find the right ones
            try:
                val = p.eval()
                print(f"  {p.name} = {val}")
            except:
                print(f"  {p.name} = (pulse/special)")
                
    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "=" * 60)
