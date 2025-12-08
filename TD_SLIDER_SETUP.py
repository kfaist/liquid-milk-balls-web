# ==============================================
# SIMPLE UDP SLIDER SETUP - PASTE IN TEXTPORT
# ==============================================

import json

# Create UDP receiver at project root
udp = op('/project1').create(udpinDAT, 'web_sliders_udp')
udp.par.port = 8021
udp.par.active = True
udp.nodeX = -400
udp.nodeY = 200

# Create table to store values
tbl = op('/project1').create(tableDAT, 'web_sliders')
tbl.nodeX = -200
tbl.nodeY = 200
tbl.clear()
tbl.appendRow(['param', 'value'])
tbl.appendRow(['hue', '280'])
tbl.appendRow(['sat', '85'])
tbl.appendRow(['val', '50'])
tbl.appendRow(['sz', '50'])
tbl.appendRow(['spd', '10'])
tbl.appendRow(['glw', '60'])
tbl.appendRow(['temp', '1'])
tbl.appendRow(['bump', '50'])
tbl.appendRow(['depth', '50'])
tbl.appendRow(['gloss', '50'])
tbl.appendRow(['emboss', '50'])
tbl.appendRow(['halo', '50'])
tbl.appendRow(['shimmer', '50'])
tbl.appendRow(['opacity', '50'])
tbl.appendRow(['velocity', '50'])

# Create CHOP to convert table to channels (easier to use!)
datto = op('/project1').create(dattoDAT, 'slider_parse')
datto.nodeX = 0
datto.nodeY = 200

# Create text DAT with execute script
exe = op('/project1').create(textDAT, 'slider_updater')
exe.nodeX = -200
exe.nodeY = 300
exe.text = '''import json
def update_sliders():
    udp = op('web_sliders_udp')
    tbl = op('web_sliders')
    if udp.numRows > 0:
        try:
            msg = udp[udp.numRows-1, 0].val
            data = json.loads(msg)
            for key, val in data.items():
                for i in range(1, tbl.numRows):
                    if tbl[i, 0].val == key:
                        tbl[i, 1] = str(val)
        except: pass
'''

print("")
print("="*50)
print("WEB SLIDERS READY!")
print("="*50)
print("Created: web_sliders_udp, web_sliders table")
print("")
print("USE IN PARAMETERS:")
print("  op('web_sliders')['hue',1]")
print("  op('web_sliders')['bump',1]")
print("="*50)
