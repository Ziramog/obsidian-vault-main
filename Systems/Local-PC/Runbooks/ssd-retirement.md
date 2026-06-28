# Runbook: Retiro Seguro del SSD Antiguo (Disco 0)

## Estado actual

- Disco 0: WDC WDS250G1B0A, SSD SATA 250 GB, MBR
- IsSystem=False, IsBoot=False (ya no es necesario para arrancar)
- Particiones: 50 MB (sistema viejo), F: 146 GB (Windows anterior), 495 MB (recovery), G: 86 GB (wolfim/proyectos)

## Prerrequisitos

- [ ] NVMe arranca autónomamente (confirmado 2026-06-23)
- [ ] Obsidian vault migrado de G: a C:\Projects\Obsidian\obsidian-vault-main\
- [ ] Datos de F:\Users\ingju\ respaldados (si se necesitan)
- [ ] Proyectos en G:\projects\ verificados contra C:\Projects\

## Procedimiento

### 1. Verificar independencia total

Apagar, desconectar físicamente el cable SATA del Disco 0. Encender. El sistema debe arrancar normalmente desde el NVMe.

### 2. Datos a recuperar antes de formatear

- `F:\Users\ingju\` — perfil del Windows anterior (Codex, Antigravity, documentos)
- `G:\projects\Obsidian\` — vault viejo (ya migrado a C:)
- `G:\projects\` — proyectos con Git (ya en C:, verificar diferencias)

### 3. Formatear y reutilizar

Una vez respaldado todo, el disco puede:
- Formatearse como un solo volumen de 233 GB para datos
- Usarse como destino de backups locales
- Dejarse como disco de reserva

### 4. Rollback

Si algo falla, reconectar el cable SATA. El Disco 0 aún tiene bootmgr y BCD funcionales. Cambiar orden de arranque en BIOS para usar el SSD.

## ⚠️ No formatear sin autorización explícita
