import webbrowser
import os

# Get the full path
file_path = os.path.abspath('verification_review.html')
print(f"Opening: {file_path}")

# Open in default browser
webbrowser.open(f'file:///{file_path}')
print("[OK] Verification review opened in browser!")
