# ==============================================
# PHOTOREALISM EFFECT - QUICK SETUP
# Paste into TouchDesigner Textport
# ==============================================
# Creates effects controlled by photorealism slider:
# - Low (0): Stylized/dreamy look
# - High (100): Sharp, detailed, realistic
# ==============================================

print("\n" + "="*50)
print("PHOTOREALISM EFFECT SETUP")
print("="*50 + "\n")

# Find the slider_values table
slider_table = op('/project1/slider_system/slider_values')
if not slider_table:
    print("[ERROR] slider_system not found!")
    print("Run TD_SLIDER_EFFECTS_SYSTEM.py first!")
else:
    # Create Sharpen TOP for photorealism
    sharp_name = 'photorealism_sharp'
    
    if op(f'/project1/{sharp_name}'):
        sharp = op(f'/project1/{sharp_name}')
        print(f"[OK] Found existing {sharp_name}")
    else:
        sharp = op('/project1').create(sharpenTOP, sharp_name)
        sharp.nodeX = 200
        sharp.nodeY = -400
        print(f"[CREATED] {sharp_name}")
    
    # Sharpness controlled by photorealism slider
    # Low photorealism = soft/dreamy (low sharpen)
    # High photorealism = crisp/detailed (high sharpen)
    sharp.par.strength.mode = ParMode.EXPRESSION
    sharp.par.strength.expr = "float(op('/project1/slider_system/slider_values')['photorealism', 'normalized']) * 2"
    
    # Create Level TOP for contrast enhancement
    level_name = 'photorealism_level'
    
    if op(f'/project1/{level_name}'):
        level = op(f'/project1/{level_name}')
        print(f"[OK] Found existing {level_name}")
    else:
        level = op('/project1').create(levelTOP, level_name)
        level.nodeX = 400
        level.nodeY = -400
        print(f"[CREATED] {level_name}")
    
    # Contrast increases with photorealism
    # Formula: 0.8 + (photorealism * 0.4) gives range 0.8-1.2
    level.par.contrast.mode = ParMode.EXPRESSION  
    level.par.contrast.expr = "0.85 + (float(op('/project1/slider_system/slider_values')['photorealism', 'normalized']) * 0.3)"
    
    # Wire them together: sharp -> level
    level.inputConnectors[0].connect(sharp)
    
    print(f"\n[OK] Photorealism effects configured!")
    print("    Sharpen strength: 0-2 based on slider")
    print("    Contrast: 0.85-1.15 based on slider")
    print("\n    Signal chain:")
    print("    [your video] -> photorealism_sharp -> photorealism_level -> [output]")
    
    print("\n" + "="*50)
    print("PHOTOREALISM SETUP COMPLETE!")
    print("="*50)
    print("\nTest: Move the 'Photorealism' slider on the web")
    print("Low = soft/dreamy, High = crisp/detailed")
