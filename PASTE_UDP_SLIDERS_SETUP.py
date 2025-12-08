# ==============================================
# PASTE THIS ENTIRE SCRIPT INTO TOUCHDESIGNER TEXTPORT
# Sets up UDP slider receiver from web interface
# ==============================================

import json

# Create container for slider system
if op('slider_system') is None:
    slider_container = parent().create(containerCOMP, 'slider_system')
    slider_container.nodeX = 400
    slider_container.nodeY = -200
else:
    slider_container = op('slider_system')

# Enter the container to create nodes inside
slider_container.allowCooking = True

# 1. Create UDP In DAT - receives from server.js
udp_in = slider_container.create(udpinDAT, 'udp_sliders')
udp_in.par.port = 8021
udp_in.par.active = True
udp_in.par.callbacks = 'slider_callbacks'
udp_in.nodeX = 0
udp_in.nodeY = 0

# 2. Create Table DAT to store parsed slider values
slider_table = slider_container.create(tableDAT, 'slider_values')
slider_table.nodeX = 300
slider_table.nodeY = 0
slider_table.clear()
# Initialize with default values
slider_table.appendRow(['parameter', 'value'])
slider_table.appendRow(['hue', '280'])
slider_table.appendRow(['sat', '85'])
slider_table.appendRow(['val', '50'])
slider_table.appendRow(['sz', '50'])
slider_table.appendRow(['spd', '10'])
slider_table.appendRow(['glw', '60'])
slider_table.appendRow(['temp', '1'])
slider_table.appendRow(['bump', '50'])
slider_table.appendRow(['depth', '50'])
slider_table.appendRow(['gloss', '50'])
slider_table.appendRow(['emboss', '50'])
slider_table.appendRow(['halo', '50'])
slider_table.appendRow(['shimmer', '50'])
slider_table.appendRow(['opacity', '50'])
slider_table.appendRow(['velocity', '50'])

# 3. Create DAT Execute for JSON parsing callbacks
callbacks_dat = slider_container.create(datexecuteDAT, 'slider_callbacks')
callbacks_dat.par.active = True
callbacks_dat.par.dat = 'udp_sliders'
callbacks_dat.par.rowchange = True
callbacks_dat.nodeX = 150
callbacks_dat.nodeY = 100

# Write the callback script
callbacks_dat.text = '''# Slider UDP Callback - parses JSON from web interface
import json

def onTableChange(dat):
    # Get the last received message
    if dat.numRows > 0:
        try:
            msg = dat[dat.numRows-1, 0].val
            data = json.loads(msg)
            
            # Update slider_values table
            table = op('slider_values')
            for key, val in data.items():
                # Find row with this parameter
                for i in range(1, table.numRows):
                    if table[i, 0].val == key:
                        table[i, 1] = str(val)
                        break
            
            print(f"Sliders updated: hue={data.get('hue')}, sat={data.get('sat')}")
        except Exception as e:
            print(f"JSON parse error: {e}")

def onRowChange(dat, rows):
    onTableChange(dat)
'''

# 4. Create Text DAT with usage instructions
usage_dat = slider_container.create(textDAT, 'USAGE')
usage_dat.nodeX = 300
usage_dat.nodeY = 150
usage_dat.text = '''
=== WEB SLIDER VALUES ===

Access slider values anywhere in your project:

  op('slider_system/slider_values')['hue', 1]
  op('slider_system/slider_values')['sat', 1]
  op('slider_system/slider_values')['bump', 1]
  etc.

Example in a Parameter expression:
  float(op('slider_system/slider_values')['hue', 1])

Or reference the whole table:
  op('slider_system/slider_values')

Available parameters:
  hue, sat, val, sz, spd, glw, temp,
  bump, depth, gloss, emboss, halo,
  shimmer, opacity, velocity
'''

print("")
print("=" * 50)
print("UDP SLIDER SYSTEM CREATED!")
print("=" * 50)
print("")
print("Components created in /slider_system:")
print("  - udp_sliders (UDP In on port 8021)")
print("  - slider_values (Table with all slider values)")
print("  - slider_callbacks (JSON parser)")
print("  - USAGE (Reference guide)")
print("")
print("Access values with:")
print("  op('slider_system/slider_values')['hue', 1]")
print("")
print("Test: Move a slider on the web interface!")
print("=" * 50)
