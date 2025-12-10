# ==============================================
# DEPTH OF FIELD EFFECT - QUICK SETUP
# Paste into TouchDesigner Textport
# ==============================================
# Creates a Blur TOP controlled by the depth slider
# Wire your video through this for DOF effect
# ==============================================

print("\n" + "="*50)
print("DEPTH OF FIELD EFFECT SETUP")
print("="*50 + "\n")

# Find the slider_values table
slider_table = op('/project1/slider_system/slider_values')
if not slider_table:
    print("[ERROR] slider_system not found!")
    print("Run TD_SLIDER_EFFECTS_SYSTEM.py first!")
else:
    # Create DOF Blur TOP at project root
    blur_name = 'dof_blur'
    
    if op(f'/project1/{blur_name}'):
        dof = op(f'/project1/{blur_name}')
        print(f"[OK] Found existing {blur_name}")
    else:
        dof = op('/project1').create(blurTOP, blur_name)
        dof.nodeX = 0
        dof.nodeY = -400
        print(f"[CREATED] {blur_name}")
    
    # Set up blur to be controlled by depth slider
    # filtersize expression pulls from slider table
    dof.par.filtertype = 'gaussian'
    dof.par.filtersize.mode = ParMode.EXPRESSION
    dof.par.filtersize.expr = "float(op('/project1/slider_system/slider_values')['depth', 'normalized']) * 30"
    
    print(f"\n[OK] {blur_name} configured!")
    print("    filtersize: 0-30 based on depth slider")
    print("\n    Wire your video INTO this blur,")
    print("    then wire OUT to your effects chain.")
    
    print("\n" + "="*50)
    print("DOF SETUP COMPLETE!")
    print("="*50)
    print(f"\nTest: Move the 'Depth of Field' slider on the web")
    print(f"The {blur_name} filtersize should change 0-30")
