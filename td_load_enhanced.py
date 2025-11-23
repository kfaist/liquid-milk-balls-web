# Load enhanced canvas test with visual feedback
wr1 = op('/project1/webrender1')
wr1.par.url = 'http://localhost:3000/enhanced_canvas_test.html'
wr1.par.reloadsrc.pulse()
print("✓ Loaded enhanced_canvas_test.html")
print("Look for blinking colored squares in corners!")
print("If corners are blinking, canvas is working")
