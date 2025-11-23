Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class WindowAPI {
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    
    [DllImport("user32.dll")]
    public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);
    
    [DllImport("user32.dll")]
    public static extern bool GetWindowText(IntPtr hWnd, StringBuilder text, int count);
    
    [DllImport("user32.dll")]
    public static extern int GetWindowTextLength(IntPtr hWnd);
}
"@

# Find OBS window
$obsWindow = [WindowAPI]::FindWindow($null, "OBS 31.0.2 (64 bit) - Profile: Untitled - Scenes: Untitled")

if ($obsWindow -eq [IntPtr]::Zero) {
    # Try different window title patterns
    $obsWindow = [WindowAPI]::FindWindow($null, "OBS")
}

if ($obsWindow -ne [IntPtr]::Zero) {
    Write-Host "Found OBS window: $obsWindow"
    [WindowAPI]::SetForegroundWindow($obsWindow)
    [WindowAPI]::ShowWindow($obsWindow, 5) # SW_SHOW
    
    # Wait a moment
    Start-Sleep -Milliseconds 500
    
    # Send hotkey for Start Streaming (usually none by default)
    # We'll try to use UI Automation instead
    Write-Host "OBS window is active"
} else {
    Write-Host "Could not find OBS window"
}
