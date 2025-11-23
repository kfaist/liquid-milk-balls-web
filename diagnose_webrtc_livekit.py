import win32com.client
import time
import json

def diagnose_td_webrtc():
    """Diagnose WebRTC and LiveKit setup in TouchDesigner"""
    
    try:
        # Connect to TouchDesigner
        td = win32com.client.Dispatch("TouchDesigner.App")
        print("✅ Connected to TouchDesigner")
        
        # Get the current project
        project = td.project
        print(f"📁 Current project: {project.name}")
        
        # Look for WebRTC and LiveKit related nodes
        webrtc_nodes = []
        livekit_nodes = []
        webrender_nodes = []
        ndi_nodes = []
        
        # Check all operators
        for op in project.findChildren(depth=100):
            op_name = op.name.lower()
            op_type = op.OPType
            
            # Check for WebRTC nodes
            if 'webrtc' in op_name or 'rtc' in op_name:
                webrtc_nodes.append({
                    'name': op.name,
                    'type': op_type,
                    'path': op.path
                })
            
            # Check for LiveKit nodes
            if 'livekit' in op_name or 'live' in op_name:
                livekit_nodes.append({
                    'name': op.name,
                    'type': op_type,
                    'path': op.path
                })
            
            # Check for WebRender nodes
            if 'webrender' in op_name or op_type == 'webrendertop':
                webrender_nodes.append({
                    'name': op.name,
                    'type': op_type,
                    'path': op.path
                })
            
            # Check for NDI nodes
            if 'ndi' in op_name or op_type in ['ndiintop', 'ndiouttop']:
                ndi_nodes.append({
                    'name': op.name,
                    'type': op_type,
                    'path': op.path
                })
        
        print("\n🔍 WEBRTC NODES FOUND:")
        if webrtc_nodes:
            for node in webrtc_nodes:
                print(f"  - {node['name']} ({node['type']}) at {node['path']}")
                # Try to check if it's active
                try:
                    op = project.findOP(node['path'])
                    if hasattr(op, 'active'):
                        print(f"    Active: {op.active}")
                    if hasattr(op, 'pars'):
                        # Check key parameters
                        for par in ['active', 'url', 'server', 'token', 'room']:
                            if hasattr(op.pars, par):
                                print(f"    {par}: {getattr(op.pars, par).eval()}")
                except:
                    pass
        else:
            print("  ❌ No WebRTC nodes found")
        
        print("\n🔍 LIVEKIT NODES FOUND:")
        if livekit_nodes:
            for node in livekit_nodes:
                print(f"  - {node['name']} ({node['type']}) at {node['path']}")
                # Check parameters
                try:
                    op = project.findOP(node['path'])
                    if hasattr(op, 'pars'):
                        for par in ['url', 'token', 'room', 'server']:
                            if hasattr(op.pars, par):
                                print(f"    {par}: {getattr(op.pars, par).eval()}")
                except:
                    pass
        else:
            print("  ❌ No LiveKit nodes found")
        
        print("\n🔍 WEBRENDER NODES FOUND:")
        if webrender_nodes:
            for node in webrender_nodes:
                print(f"  - {node['name']} ({node['type']}) at {node['path']}")
                # Check WebRender TOP parameters
                try:
                    op = project.findOP(node['path'])
                    if hasattr(op, 'pars'):
                        for par in ['httpport', 'httpaddress', 'active']:
                            if hasattr(op.pars, par):
                                print(f"    {par}: {getattr(op.pars, par).eval()}")
                except:
                    pass
        else:
            print("  ⚠️ No WebRender nodes found")
        
        print("\n🔍 NDI NODES FOUND:")
        if ndi_nodes:
            for node in ndi_nodes:
                print(f"  - {node['name']} ({node['type']}) at {node['path']}")
                # Check NDI parameters
                try:
                    op = project.findOP(node['path'])
                    if hasattr(op, 'pars'):
                        for par in ['active', 'ndiname', 'sourcename']:
                            if hasattr(op.pars, par):
                                print(f"    {par}: {getattr(op.pars, par).eval()}")
                except:
                    pass
        else:
            print("  ⚠️ No NDI nodes found")
        
        # Check for Web Render TOP specifically
        print("\n🌐 Checking for Web Render TOP:")
        webrender_top = project.findOP('*/webrender*')
        if webrender_top:
            print(f"  ✅ Found: {webrender_top.path}")
            if hasattr(webrender_top, 'pars'):
                print(f"  HTTP Port: {webrender_top.pars.httpport.eval() if hasattr(webrender_top.pars, 'httpport') else 'N/A'}")
                print(f"  Active: {webrender_top.pars.active.eval() if hasattr(webrender_top.pars, 'active') else 'N/A'}")
        
        # Look for any TOP operators that might be video sources
        print("\n📹 Video Source TOPs:")
        for op in project.findChildren(depth=100):
            if op.OPType in ['videodevin', 'moviefilein', 'webcam', 'videoin']:
                print(f"  - {op.name} ({op.OPType}) at {op.path}")
        
        print("\n✅ Diagnosis complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_td_webrtc()
