# Script to run INSIDE TouchDesigner textport
# Copy and paste these commands into TouchDesigner's textport

# Get the WebRender TOP
wr = op('/webrender_livekit_input')
print('=' * 60)
print('WEBRENDER TOP FOUND:', wr)
print('=' * 60)

# List ALL parameters with their current values
print('\nALL WEBRENDER PARAMETERS:')
for p in wr.pars():
    print(f'  {p.name}: {p.val}')

# Focus on media/enable related parameters
print('\n' + '=' * 60)
print('MEDIA/ENABLE RELATED PARAMETERS:')
print('=' * 60)
media_params = [p for p in wr.pars() if 'media' in p.name.lower() or 'enable' in p.name.lower() or 'audio' in p.name.lower()]
for p in media_params:
    print(f'  {p.name}: {p.val} (label: {p.label})')

# Check URL parameter
print('\n' + '=' * 60)
print('URL PARAMETERS:')
print('=' * 60)
url_params = [p for p in wr.pars() if 'url' in p.name.lower()]
for p in url_params:
    print(f'  {p.name}: {p.val}')

# Check reload parameters
print('\n' + '=' * 60)
print('RELOAD PARAMETERS:')
print('=' * 60)
reload_params = [p for p in wr.pars() if 'reload' in p.name.lower() or 'refresh' in p.name.lower()]
for p in reload_params:
    print(f'  {p.name}: {p.val}')

print('\n' + '=' * 60)
print('DISCOVERY COMPLETE')
print('=' * 60)
