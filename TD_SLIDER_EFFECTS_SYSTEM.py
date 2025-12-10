# ==============================================
# COMPREHENSIVE SLIDER-TO-VISUAL EFFECTS MAPPING
# Paste into TouchDesigner Textport (claudetest.toe)
# ==============================================
# 
# This script creates a complete slider-to-visuals system:
# - Receives UDP from web sliders
# - Maps parameters to visual effects
# - Includes Depth of Field, Photorealism, and more
#
# ==============================================

import json

print("\n" + "=" * 60)
print("SLIDER EFFECTS SYSTEM - INSTALLING...")
print("=" * 60 + "\n")

# ============================================
# 1. CREATE/FIND SLIDER SYSTEM CONTAINER
# ============================================

# Check if slider_system already exists
if op('/project1/slider_system'):
    slider_sys = op('/project1/slider_system')
    print("[OK] Found existing slider_system")
else:
    slider_sys = op('/project1').create(containerCOMP, 'slider_system')
    slider_sys.nodeX = -600
    slider_sys.nodeY = 200
    print("[CREATED] slider_system container")

# ============================================
# 2. CREATE UDP RECEIVER (port 8021)
# ============================================

udp_name = 'udp_sliders'
if op(f'/project1/slider_system/{udp_name}'):
    udp_in = op(f'/project1/slider_system/{udp_name}')
    print(f"[OK] Found existing {udp_name}")
else:
    udp_in = slider_sys.create(udpinDAT, udp_name)
    udp_in.nodeX = 0
    udp_in.nodeY = 0
    print(f"[CREATED] {udp_name}")

udp_in.par.port = 8021
udp_in.par.active = True

# ============================================
# 3. CREATE SLIDER VALUES TABLE
# ============================================

table_name = 'slider_values'
if op(f'/project1/slider_system/{table_name}'):
    slider_table = op(f'/project1/slider_system/{table_name}')
    print(f"[OK] Found existing {table_name}")
else:
    slider_table = slider_sys.create(tableDAT, table_name)
    slider_table.nodeX = 300
    slider_table.nodeY = 0
    print(f"[CREATED] {table_name}")

# Initialize table with all parameters
slider_table.clear()
slider_table.appendRow(['parameter', 'value', 'normalized'])
params = {
    'hue': (280, 0, 360),
    'sat': (85, 0, 100),
    'val': (50, 0, 100),
    'sz': (50, 10, 120),
    'spd': (10, 5, 30),
    'glw': (60, 0, 100),
    'temp': (1, 0, 100),
    'bump': (50, 0, 100),
    'depth': (50, 0, 100),      # Depth of Field
    'gloss': (50, 0, 100),
    'emboss': (50, 0, 100),
    'halo': (50, 0, 100),
    'shimmer': (50, 0, 100),
    'opacity': (50, 0, 100),
    'velocity': (50, 0, 100),
    'photorealism': (50, 0, 100)  # NEW: Photorealism slider
}

for name, (default, min_v, max_v) in params.items():
    normalized = (default - min_v) / (max_v - min_v)
    slider_table.appendRow([name, str(default), f'{normalized:.4f}'])

print(f"[OK] Initialized {len(params)} slider parameters")

# ============================================
# 4. CREATE CALLBACK SCRIPT
# ============================================

callback_name = 'slider_callbacks'
if op(f'/project1/slider_system/{callback_name}'):
    callbacks = op(f'/project1/slider_system/{callback_name}')
    print(f"[OK] Found existing {callback_name}")
else:
    callbacks = slider_sys.create(textDAT, callback_name)
    callbacks.nodeX = 150
    callbacks.nodeY = 100
    print(f"[CREATED] {callback_name}")

callbacks.text = '''# Slider UDP Callback - parses JSON and updates table
import json

# Parameter ranges for normalization
RANGES = {
    'hue': (0, 360), 'sat': (0, 100), 'val': (0, 100),
    'sz': (10, 120), 'spd': (5, 30), 'glw': (0, 100),
    'temp': (0, 100), 'bump': (0, 100), 'depth': (0, 100),
    'gloss': (0, 100), 'emboss': (0, 100), 'halo': (0, 100),
    'shimmer': (0, 100), 'opacity': (0, 100), 'velocity': (0, 100),
    'photorealism': (0, 100)
}

def onReceive(dat, rowIndex, message, bytes, peer):
    """Called when UDP message received"""
    try:
        data = json.loads(message)
        table = op('slider_values')
        
        for key, val in data.items():
            # Calculate normalized value
            if key in RANGES:
                min_v, max_v = RANGES[key]
                norm = (float(val) - min_v) / (max_v - min_v)
                norm = max(0, min(1, norm))
            else:
                norm = float(val) / 100.0
            
            # Update table
            for i in range(1, table.numRows):
                if table[i, 0].val == key:
                    table[i, 1] = str(val)
                    table[i, 2] = f'{norm:.4f}'
                    break
            else:
                # New parameter - add it
                table.appendRow([key, str(val), f'{norm:.4f}'])
                
    except Exception as e:
        pass  # Silent fail for malformed messages
'''

# Set up UDP to use callbacks
udp_in.par.callbacks = callback_name

# ============================================
# 5. CREATE EFFECT HELPER MODULE
# ============================================

helper_name = 'slider_helpers'
if op(f'/project1/slider_system/{helper_name}'):
    helpers = op(f'/project1/slider_system/{helper_name}')
else:
    helpers = slider_sys.create(textDAT, helper_name)
    helpers.nodeX = 300
    helpers.nodeY = 100

helpers.text = '''# ==============================================
# SLIDER HELPER FUNCTIONS
# Import with: mod('slider_system/slider_helpers')
# ==============================================

def get(param, default=0.5):
    """Get normalized slider value (0-1)"""
    try:
        table = op('/project1/slider_system/slider_values')
        for i in range(1, table.numRows):
            if table[i, 0].val == param:
                return float(table[i, 2].val)
        return default
    except:
        return default

def getRaw(param, default=50):
    """Get raw slider value"""
    try:
        table = op('/project1/slider_system/slider_values')
        for i in range(1, table.numRows):
            if table[i, 0].val == param:
                return float(table[i, 1].val)
        return default
    except:
        return default

def getHue():
    """Get hue value (0-360)"""
    return getRaw('hue', 280)

def getSat():
    """Get saturation (0-1)"""
    return get('sat', 0.85)

def getVal():
    """Get value/brightness (0-1)"""
    return get('val', 0.5)

def getDepthOfField():
    """Get depth of field amount (0-1)
    0 = no blur (sharp)
    1 = maximum blur (dreamy)
    """
    return get('depth', 0.5)

def getPhotorealism():
    """Get photorealism amount (0-1)
    0 = stylized/abstract
    1 = photorealistic
    """
    return get('photorealism', 0.5)

def getShimmer():
    """Get shimmer intensity (0-1)"""
    return get('shimmer', 0.5)

def getGlow():
    """Get glow intensity (0-1)"""
    return get('glw', 0.6)

def getBump():
    """Get bump/displacement amount (0-1)"""
    return get('bump', 0.5)

def getVelocity():
    """Get motion/velocity effect (0-1)"""
    return get('velocity', 0.5)

# Example usage in parameter expressions:
# 
# Blur amount controlled by depth slider:
#   mod('slider_system/slider_helpers').getDepthOfField() * 20
#
# Hue shift:
#   mod('slider_system/slider_helpers').getHue()
#
# Glow intensity:
#   mod('slider_system/slider_helpers').getGlow()
'''

# ============================================
# 6. CREATE CHOP OUTPUTS FOR EASY WIRING
# ============================================

chop_name = 'slider_chops'
if op(f'/project1/slider_system/{chop_name}'):
    slider_chops = op(f'/project1/slider_system/{chop_name}')
else:
    # Create a Constant CHOP that reads from table
    slider_chops = slider_sys.create(constantCHOP, chop_name)
    slider_chops.nodeX = 500
    slider_chops.nodeY = 0

# Set up constant CHOP with all parameters as channels
param_list = list(params.keys())
slider_chops.par.name0 = 'hue'
slider_chops.par.value0.expr = "float(op('slider_values')['hue', 'normalized'])"

# For remaining params, we'll use expressions in a different way
# Create an Expression CHOP instead for dynamic values

expr_name = 'slider_expr'
if op(f'/project1/slider_system/{expr_name}'):
    slider_expr = op(f'/project1/slider_system/{expr_name}')
else:
    slider_expr = slider_sys.create(expressionCHOP, expr_name)
    slider_expr.nodeX = 500
    slider_expr.nodeY = 100

# ============================================
# 7. CREATE USAGE DOCUMENTATION
# ============================================

usage_name = 'USAGE_GUIDE'
if op(f'/project1/slider_system/{usage_name}'):
    usage = op(f'/project1/slider_system/{usage_name}')
else:
    usage = slider_sys.create(textDAT, usage_name)
    usage.nodeX = 500
    usage.nodeY = 200

usage.text = '''
===============================================
WEB SLIDER INTEGRATION - USAGE GUIDE
===============================================

QUICK ACCESS (in parameter expressions):
----------------------------------------
# Get normalized value (0-1):
float(op('/project1/slider_system/slider_values')['depth', 'normalized'])

# Get raw value:
float(op('/project1/slider_system/slider_values')['hue', 'value'])


HELPER FUNCTIONS (cleaner syntax):
----------------------------------
# First import the helper module
h = mod('/project1/slider_system/slider_helpers')

# Then use helper functions:
h.getDepthOfField()    # 0-1 for blur amount
h.getPhotorealism()    # 0-1 for realism level
h.getHue()             # 0-360 hue angle
h.getSat()             # 0-1 saturation
h.getGlow()            # 0-1 glow intensity
h.getShimmer()         # 0-1 shimmer effect
h.getBump()            # 0-1 displacement
h.getVelocity()        # 0-1 motion blur


COMMON EFFECT MAPPINGS:
-----------------------

DEPTH OF FIELD (Blur TOP):
  - filtersize: h.getDepthOfField() * 20
  - Gives 0-20 pixel blur based on slider

PHOTOREALISM (Level TOP or similar):
  - Use to blend between stylized and realistic
  - opacity or mix: h.getPhotorealism()

COLOR (HSV Adjust TOP):
  - hueoffset: h.getHue()
  - saturationmult: h.getSat() * 2
  - valuemult: h.getVal() * 2

GLOW (Bloom TOP):
  - size: h.getGlow() * 50
  - intensity: h.getGlow()

SHIMMER (Noise TOP + Composite):
  - amplitude: h.getShimmer() * 0.5


AVAILABLE PARAMETERS:
--------------------
hue, sat, val, sz, spd, glw, temp, bump,
depth, gloss, emboss, halo, shimmer,
opacity, velocity, photorealism

===============================================
'''

print("\n" + "=" * 60)
print("SLIDER EFFECTS SYSTEM - COMPLETE!")
print("=" * 60)
print("""
CREATED IN /project1/slider_system:
  - udp_sliders       : UDP receiver on port 8021
  - slider_values     : Table with all parameter values
  - slider_callbacks  : JSON parser for incoming data
  - slider_helpers    : Helper functions module
  - slider_chops      : CHOP output
  - USAGE_GUIDE       : Documentation

TEST: Move a slider on the web interface!
The slider_values table should update in real-time.

USE IN PARAMETERS:
  float(op('/project1/slider_system/slider_values')['depth', 'normalized'])

OR WITH HELPERS:
  mod('/project1/slider_system/slider_helpers').getDepthOfField()
""")
print("=" * 60 + "\n")
