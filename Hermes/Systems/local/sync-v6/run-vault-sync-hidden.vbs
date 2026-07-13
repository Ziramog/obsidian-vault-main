Option Explicit
Dim shell, cmd, rc
Set shell = CreateObject("WScript.Shell")
cmd = """C:\Users\ingju\AppData\Local\hermes\git\usr\bin\bash.exe"" -lc ""'/c/Users/ingju/.local/bin/hermes-vault-sync' --sync"""
rc = shell.Run(cmd, 0, True)
WScript.Quit rc
