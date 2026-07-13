Option Explicit
Dim shell, bashPath, cmd, rc
bashPath = "C:\Users\ingju\AppData\Local\hermes\git\usr\bin\bash.exe"
cmd = """" & bashPath & """" & " -lc " & """" & "~/.local/bin/hermes-vault-sync --sync" & """"
Set shell = CreateObject("WScript.Shell")
rc = shell.Run(cmd, 0, True)
WScript.Quit rc
