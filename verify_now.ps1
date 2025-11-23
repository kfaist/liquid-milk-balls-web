
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class WinAPI {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
    }
"@

$td = Get-Process -Name "TouchDesigner" -ErrorAction SilentlyContinue
if ($td) {
    [WinAPI]::SetForegroundWindow($td.MainWindowHandle) | Out-Null
    Start-Sleep -Milliseconds 500
    
    [System.Windows.Forms.SendKeys]::SendWait("%t")
    Start-Sleep -Milliseconds 800
    
    [System.Windows.Forms.SendKeys]::SendWait("^a")
    Start-Sleep -Milliseconds 200
    
    $cmd = "exec(open('C:/Users/krista-showputer/Desktop/liquid-milk-balls-web/td_verify_to_file.py').read())"
    [System.Windows.Forms.SendKeys]::SendWait($cmd)
    Start-Sleep -Milliseconds 400
    
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 2000
}
