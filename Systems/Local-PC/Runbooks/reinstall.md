# Runbook: Reinstalación de Windows y Herramientas

## Orden de instalación

### 1. Windows 10 Pro

- USB: `Win_10_Pro_19045_4651` (Kingston DataTraveler 3.0)
- Instalar en Disco 2 (WD PC SN740, NVMe 512 GB)
- Modo Legacy/MBR (siempre que la BIOS esté en Legacy/CSM)

### 2. Drivers

- GPU: NVIDIA GeForce RTX 3070 Ti → GeForce Experience o driver manual
- Chipset: Intel H110 → Windows Update o sitio ASRock
- Red, audio: Windows Update

### 3. Navegador

- Chrome: `ChromeSetup.exe` en `Downloads\`

### 4. Git y GitHub CLI

```
winget install Git.Git
winget install GitHub.cli
gh auth login
gh auth setup-git
```

### 5. Node.js

- v22 LTS: `winget install OpenJS.NodeJS.LTS`
- O usar el que instala Hermes

### 6. Python y uv

```
winget install Python.Python.3.11
winget install astral-sh.uv
```

### 7. Hermes Agent

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### 8. Codex

- Instalador: `Codex Installer.exe` en `Downloads\`
- App de Windows Store o instalación directa

### 9. Antigravity IDE

- Instalador en `Downloads\`: `Antigravity-x64.exe`
- O `Antigravity IDE.exe`

### 10. OpenCode Desktop

- Descargar desde sitio oficial
- El updater detecta instalación previa en `AppData\Local\@opencode-aidesktop-updater`

### 11. Obsidian

- Portable: copiar carpeta `C:\Projects\Obsidian\` desde backup
- Vault: apuntar a `C:\Projects\Obsidian\obsidian-vault-main\`

### 12. VS Code (opcional)

- Portable en `C:\Projects\Microsoft VS Code\`

## Post-instalación

- [ ] Configurar teclado español latino: `Get-WinUserLanguageList` + `Add`
- [ ] `gh auth login` y `gh auth setup-git`
- [ ] Restaurar `.codex\`, configs de Antigravity, OpenCode desde backup
- [ ] Restaurar vault Obsidian
- [ ] Ejecutar `monitor-login.ps1` para verificar estado
