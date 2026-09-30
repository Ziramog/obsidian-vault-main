Option Explicit
Dim shell, bashPath, scriptPath, cmd, rc
bashPath = "C:\Users\ingju\AppData\Local\hermes\git\usr\bin\bash.exe"
scriptPath = "C:\Projects\Obsidian\obsidian-vault-main\Hermes\Systems\local\scripts\hermes-model-routing-guard.sh"
cmd = """" & bashPath & """" & " " & """" & scriptPath & """"
Set shell = CreateObject("WScript.Shell")

Do
  rc = shell.Run(cmd, 0, True)
  WScript.Sleep 3600000
Loop
