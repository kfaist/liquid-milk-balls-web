# ==============================================
# COMPLETE SLIDER-CONTROLLED EFFECTS CHAIN
# Paste into TouchDesigner Textport (claudetest.toe)
# ==============================================
# Creates a full video effects pipeline:
# [INPUT] -> DOF -> Photorealism -> Color -> Glow -> [OUTPUT]
# All controlled by web sliders!
# ==============================================

print("\n" + "="*60)
print("COMPLETE EFFECTS CHAIN SETUP")
print("="*60 + "\n")

# Check for slider system
if not op('/project1/slider_system/slider_values'):
    print("[ERROR] Run TD_SLIDER_EFFECTS_SYSTEM.py first!")
    print("That creates the slider receiver system.")
else:
    # Base position for effects chain
    base_x = -400
    base_y = -600
    spacing = 250

    # ==========================================
    # 1. INPUT NULL (wire your video here)
    # ==========================================
    if op('/project1/effects_input'):
        fx_in = op('/project1/effects_input')
    else:
        fx_in = op('/project1').create(nullTOP, 'effects_input')
        fx_in.nodeX = base_x
        fx_in.nodeY = base_y
    print("[1] effects_input - WIRE YOUR VIDEO HERE")

    # ==========================================
    # 2. DEPTH OF FIELD (Blur)
    # ==========================================
    if op('/project1/fx_dof'):
        dof = op('/project1/fx_dof')
    else:
        dof = op('/project1').create(blurTOP, 'fx_dof')
        dof.nodeX = base_x + spacing
        dof.nodeY = base_y
    
    dof.par.filtertype = 'gaussian'
    dof.par.filtersize.mode = ParMode.EXPRESSION
    dof.par.filtersize.expr = "float(op('/project1/slider_system/slider_values')['depth', 'normalized']) * 25"
    dof.inputConnectors[0].connect(fx_in)
    print("[2] fx_dof - Depth of Field (blur 0-25)")

    # ==========================================
    # 3. SHARPEN (Photorealism detail)
    # ==========================================
    if op('/project1/fx_sharpen'):
        sharp = op('/project1/fx_sharpen')
    else:
        sharp = op('/project1').create(sharpenTOP, 'fx_sharpen')
        sharp.nodeX = base_x + spacing*2
        sharp.nodeY = base_y
    
    sharp.par.strength.mode = ParMode.EXPRESSION
    sharp.par.strength.expr = "float(op('/project1/slider_system/slider_values')['photorealism', 'normalized']) * 1.5"
    sharp.inputConnectors[0].connect(dof)
    print("[3] fx_sharpen - Photorealism sharpness (0-1.5)")

    # ==========================================
    # 4. LEVEL (Contrast/Brightness)
    # ==========================================
    if op('/project1/fx_level'):
        level = op('/project1/fx_level')
    else:
        level = op('/project1').create(levelTOP, 'fx_level')
        level.nodeX = base_x + spacing*3
        level.nodeY = base_y
    
    # Contrast from photorealism
    level.par.contrast.mode = ParMode.EXPRESSION
    level.par.contrast.expr = "0.9 + (float(op('/project1/slider_system/slider_values')['photorealism', 'normalized']) * 0.2)"
    # Brightness from val slider
    level.par.brightness1.mode = ParMode.EXPRESSION
    level.par.brightness1.expr = "(float(op('/project1/slider_system/slider_values')['val', 'normalized']) - 0.5) * 0.3"
    level.inputConnectors[0].connect(sharp)
    print("[4] fx_level - Contrast & brightness")

    # ==========================================
    # 5. HSV ADJUST (Color)
    # ==========================================
    if op('/project1/fx_hsv'):
        hsv = op('/project1/fx_hsv')
    else:
        hsv = op('/project1').create(hsvadjustTOP, 'fx_hsv')
        hsv.nodeX = base_x + spacing*4
        hsv.nodeY = base_y
    
    # Hue offset from hue slider (shift by slider value)
    hsv.par.hueoffset.mode = ParMode.EXPRESSION
    hsv.par.hueoffset.expr = "(float(op('/project1/slider_system/slider_values')['hue', 'value']) - 180) / 360"
    # Saturation from sat slider
    hsv.par.saturationmult.mode = ParMode.EXPRESSION
    hsv.par.saturationmult.expr = "float(op('/project1/slider_system/slider_values')['sat', 'normalized']) * 2"
    hsv.inputConnectors[0].connect(level)
    print("[5] fx_hsv - Hue & saturation")

    # ==========================================
    # 6. BLOOM/GLOW
    # ==========================================
    if op('/project1/fx_bloom'):
        bloom = op('/project1/fx_bloom')
    else:
        bloom = op('/project1').create(bloomTOP, 'fx_bloom')
        bloom.nodeX = base_x + spacing*5
        bloom.nodeY = base_y
    
    bloom.par.size.mode = ParMode.EXPRESSION
    bloom.par.size.expr = "float(op('/project1/slider_system/slider_values')['glw', 'normalized']) * 40"
    bloom.par.intensity.mode = ParMode.EXPRESSION
    bloom.par.intensity.expr = "float(op('/project1/slider_system/slider_values')['glw', 'normalized']) * 0.5"
    bloom.inputConnectors[0].connect(hsv)
    print("[6] fx_bloom - Glow effect")

    # ==========================================
    # 7. OUTPUT NULL
    # ==========================================
    if op('/project1/effects_output'):
        fx_out = op('/project1/effects_output')
    else:
        fx_out = op('/project1').create(nullTOP, 'effects_output')
        fx_out.nodeX = base_x + spacing*6
        fx_out.nodeY = base_y
    
    fx_out.inputConnectors[0].connect(bloom)
    print("[7] effects_output - FINAL OUTPUT")

    print("\n" + "="*60)
    print("EFFECTS CHAIN COMPLETE!")
    print("="*60)
    print("""
SIGNAL CHAIN:
  effects_input -> fx_dof -> fx_sharpen -> fx_level -> fx_hsv -> fx_bloom -> effects_output

CONTROLLED BY SLIDERS:
  - Depth of Field: blur amount
  - Photorealism: sharpness + contrast
  - Value: brightness
  - Hue: color shift
  - Saturation: color intensity
  - Glow: bloom size & intensity

TO USE:
  1. Wire your video source INTO 'effects_input'
  2. Wire 'effects_output' to your NDI out or display
  3. Move sliders on the web interface!
""")
    print("="*60 + "\n")
