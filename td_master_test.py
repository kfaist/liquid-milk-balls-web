# MASTER TEST RUNNER
# This will load each test page and wait for you to observe

import time

print("=" * 70)
print("MASTER WEBRENDER VIDEO TEST RUNNER")
print("By Claude - Running systematic diagnostics")
print("=" * 70)

wr1 = op('/project1/webrender1')

tests = [
    {
        'name': 'Baseline: Simple Color Test',
        'url': 'http://localhost:3000/simple_color_test.html',
        'what_to_look_for': 'Rainbow gradient background with white box and clock',
        'success_means': 'WebRender can display HTML/CSS'
    },
    {
        'name': 'Ultra Verbose Diagnostic',
        'url': 'http://localhost:3000/ultra_verbose_test.html',
        'what_to_look_for': 'Green text log showing all video element states',
        'success_means': 'Can see detailed diagnostics of video initialization'
    },
    {
        'name': 'Canvas-Based Video',
        'url': 'http://localhost:3000/canvas_video_test.html',
        'what_to_look_for': 'Video drawn to canvas with green overlay showing frame count',
        'success_means': 'CEF can render canvas with video frames'
    },
    {
        'name': 'Force Video Element',
        'url': 'http://localhost:3000/force_video.html',
        'what_to_look_for': 'Green info box showing videoWidth/videoHeight',
        'success_means': 'Video element itself works in CEF'
    }
]

print(f"\nRunning {len(tests)} tests on: {wr1.path}")
print(f"Current URL: {wr1.par.url.eval()}\n")

for i, test in enumerate(tests, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}/{len(tests)}: {test['name']}")
    print(f"{'='*70}")
    print(f"Loading: {test['url']}")
    print(f"Look for: {test['what_to_look_for']}")
    print(f"Success means: {test['success_means']}")
    
    # Load the test
    wr1.par.url = test['url']
    wr1.par.reloadsrc.pulse()
    
    print(f"\n✓ Loaded. TOP output: {wr1.width}x{wr1.height}")
    print(f"⏸  PAUSED - Take a screenshot and observe")
    print(f"   Then type 'c' to continue to next test\n")
    
    # In a real interactive environment, we'd wait for input
    # For now, just document the test

print(f"\n{'='*70}")
print("ALL TESTS LOADED")
print(f"{'='*70}")
print(f"\nFinal state:")
print(f"  Current URL: {wr1.par.url.eval()}")
print(f"  TOP dimensions: {wr1.width}x{wr1.height}")
print(f"  Media stream enabled: {wr1.par.mediastream.eval()}")
print(f"  Cache directory: {wr1.par.userdir.eval()}")

print(f"\n{'='*70}")
print("NEXT STEPS:")
print("1. Take screenshots of each test")
print("2. Note which tests show video vs which don't")
print("3. Check TD Console (Dialogs → Console) for errors")
print("4. Report back which test worked (if any)")
print(f"{'='*70}")
