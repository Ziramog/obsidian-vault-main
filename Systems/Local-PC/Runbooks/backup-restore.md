# Runbook: Restauración de Backups

## Ubicaciones de backup

| Ubicación | Contenido | Fecha |
|-----------|-----------|-------|
| `C:\Backups\Boot\` | BCD e inventario pre-intervención | 2026-06-23 |
| `I:\roggero_backup\` | Backups de usuario (tar.gz) | 2026-06-20 |
| `I:\roggero_backup_*.tar.gz` | Backup individual | 2026-06-20 |
| `D:\Drivers Backup\` | Drivers y archivos ZIP | Varias |
| `D:\Photos 1-4.zip` | Fotos | — |

## Procedimiento de restauración

### Restaurar BCD

```
bcdedit /import C:\Backups\Boot\BCD-backup-20260623-184256.bcd
```

### Restaurar proyectos desde tar.gz

```
tar -xzf I:\roggero_backup\roggero_backup_2026-06-20_123320.tar.gz -C C:\Projects\
```

### Restaurar Hermes profile

1. Reinstalar Hermes Agent.
2. Copiar el perfil pcbrain desde el backup:
   ```
   robocopy <backup>\hermes-pcbrain C:\Users\ingju\AppData\Local\hermes\profiles\pcbrain /MIR
   ```

### Restaurar configs de herramientas

- Codex: copiar `.codex\` desde backup al home
- Antigravity: copiar `AppData\Roaming\Antigravity*\` desde backup
- OpenCode: copiar `AppData\Roaming\ai.opencode.desktop\` desde backup

## Verificación post-restauración

- [ ] `C:\Projects\` contiene los 40 proyectos
- [ ] `git status` en cada repo con remote
- [ ] Hermes arranca con `hermes --continue`
- [ ] Obsidian vault accesible
