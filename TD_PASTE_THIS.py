# PASTE IN TOUCHDESIGNER TEXTPORT
# Polls Railway server for web slider values

# 1. Web DAT to fetch slider state
web = parent().create(webDAT, 'slider_fetch')
web.par.url = 'https://adequate-balance-production.up.railway.app/api/sliders'
web.par.fetchperiod = 0.1  # Poll 10x per second
web.par.fetchmethod = 'Automatic'
web.nodeX = 0
web.nodeY = 0

# 2. Table to store parsed values
t = parent().create(tableDAT, 'slider_values')
t.nodeX = 200
t.nodeY = 0
t.clear()
t.appendRow(['param','value'])
for p,v in [('hue',280),('sat',85),('val',50),('sz',50),('spd',10),('glw',60),('temp',1),('bump',50),('depth',50),('gloss',50),('emboss',50),('halo',50),('shimmer',50),('opacity',50),('velocity',50)]:
    t.appendRow([p,str(v)])

# 3. DAT Execute to parse JSON responses
ex = parent().create(datexecuteDAT, 'slider_parser')
ex.par.dat = 'slider_fetch'
ex.par.tablechange = True
ex.par.active = True
ex.nodeX = 100
ex.nodeY = 100
ex.text = '''import json
def onTableChange(dat):
    if dat.numRows < 1: return
    try:
        raw = dat[0,0].val
        if not raw.startswith('{'): return
        d = json.loads(raw)
        t = op('slider_values')
        for k,v in d.items():
            for i in range(1,t.numRows):
                if t[i,0].val==k: t[i,1]=str(v)
    except Exception as e:
        debug("Parse error:", e)
'''

print("")
print("="*50)
print("WEB SLIDERS READY!")
print("="*50)
print("Polling: https://adequate-balance-production.up.railway.app/api/sliders")
print("")
print("USE IN PARAMETERS:")
print("  op('slider_values')['hue',1]")
print("  op('slider_values')['bump',1]")
print("  op('slider_values')['opacity',1]")
print("="*50)
