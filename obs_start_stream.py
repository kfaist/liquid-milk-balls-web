import obsws_python as obs
import time

try:
    print('Connecting to OBS WebSocket...')
    client = obs.ReqClient(host='localhost', port=4455, password='')
    print('Connected!\n')
    
    # Get current streaming status
    try:
        status = client.get_stream_status()
        print(f'Current stream status: {status.output_active}')
    except Exception as e:
        print(f'Could not get stream status: {e}')
    
    # Start streaming
    print('\nStarting stream...')
    try:
        client.start_stream()
        print('Stream command sent!')
        
        # Wait a moment
        time.sleep(3)
        
        # Check status again
        status = client.get_stream_status()
        print(f'Stream active: {status.output_active}')
        
        if status.output_active:
            print('\nSUCCESS! Stream is now active!')
        else:
            print('\nStream failed to start - check OBS logs')
            
    except Exception as e:
        print(f'Error starting stream: {e}')
    
    client.disconnect()
    
except Exception as e:
    print(f'Error: {e}')
    print('\nMake sure:')
    print('1. OBS is running')
    print('2. WebSocket server is enabled')
    print('3. No password is set')
