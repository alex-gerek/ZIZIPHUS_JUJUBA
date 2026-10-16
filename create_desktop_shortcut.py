"""
Creates a bulletproof Desktop shortcut for ZIZIPHUS JUJUBA.
Target: C:\\Windows\\System32\\cmd.exe /c start.bat
Working directory: D:\\Projects\\ZIZIPHUS_JUJUBA
Icon: C:\\Windows\\System32\\shell32.dll,23
"""

import os
import pathlib
import subprocess

desktop = pathlib.Path(os.path.expanduser('~')) / 'Desktop'
working_dir = pathlib.Path(__file__).resolve().parent
shortcut_path = desktop / 'ZIZIPHUS JUJUBA.lnk'

ps_code = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = 'C:\\Windows\\System32\\cmd.exe'
$Shortcut.Arguments = '/k start.bat'
$Shortcut.WorkingDirectory = '{working_dir}'
$Shortcut.Description = 'ZIZIPHUS JUJUBA: Signal Intelligence Lab'
$Shortcut.IconLocation = 'C:\\Windows\\System32\\shell32.dll,23'
$Shortcut.Save()
"""

res = subprocess.run(['powershell', '-NoProfile', '-Command', ps_code], capture_output=True, text=True)
if res.returncode == 0:
    print(f"Success: Shortcut created at {shortcut_path}")
else:
    print(f"Error: {res.stderr}")
