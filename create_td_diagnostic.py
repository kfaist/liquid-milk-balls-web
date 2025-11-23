"""
Diagnostic script to discover WebRender TOP parameters
This will save output to a file instead of using PyAutoGUI
"""
import subprocess
import time

# Create a Python script to execute in TouchDesigner
td_script = """
import sys
sys.path.append('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web')

# Redirect output to file
output_file = 'C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrender_params_output.txt'
with open(output_file, 'w') as f:
    sys.stdout = f
    
    try:
        # Get the WebRender TOP
        wr = op('/webrender_livekit_input')
        print('=' * 80)
        print('WEBRENDER TOP DISCOVERY')
        print('=' * 80)
        print(f'Operator found: {wr}')
        print(f'Operator type: {type(wr)}')
        print()
        
        # List ALL parameters
        print('ALL PARAMETERS:')
        print('-' * 80)
        for p in wr.pars():
            print(f'{p.name:30s} = {p.val}')
        print()
        
        # Media/Enable related
        print('MEDIA/ENABLE/AUDIO PARAMETERS:')
        print('-' * 80)
        media_params = [p for p in wr.pars() if any(keyword in p.name.lower() for keyword in ['media', 'enable', 'audio', 'microphone', 'camera'])]
        for p in media_params:
            print(f'{p.name:30s} = {p.val:15s} (label: {p.label})')
        print()
        
        # URL parameters
        print('URL PARAMETERS:')
        print('-' * 80)
        url_params = [p for p in wr.pars() if 'url' in p.name.lower()]
        for p in url_params:
            print(f'{p.name:30s} = {p.val}')
        print()
        
        # Reload parameters
        print('RELOAD/REFRESH PARAMETERS:')
        print('-' * 80)
        reload_params = [p for p in wr.pars() if any(keyword in p.name.lower() for keyword in ['reload', 'refresh', 'pulse'])]
        for p in reload_params:
            print(f'{p.name:30s} = {p.val}')
        print()
        
        print('=' * 80)
        print('DISCOVERY COMPLETE')
        print('=' * 80)
        
    except Exception as e:
        print(f'ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
    
    sys.stdout = sys.__stdout__

print('Output saved to: C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/webrender_params_output.txt')
"""

# Save the script
with open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_execute_diagnostic.py', 'w') as f:
    f.write(td_script)

print("Diagnostic script created: td_execute_diagnostic.py")
print("\nNEXT STEPS:")
print("1. Copy the contents of td_execute_diagnostic.py")
print("2. Paste into TouchDesigner's textport (Alt+T)")
print("3. The output will be saved to webrender_params_output.txt")
print("\nOr we can use alternative methods to query TouchDesigner...")
