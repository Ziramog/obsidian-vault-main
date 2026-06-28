# Runbook: Recuperación del arranque Legacy/MBR del NVMe

## Escenario

El sistema no arranca desde el NVMe (Disco 2, WD PC SN740). Windows está en C: pero el boot manager falla.

## Síntomas

- "Boot Device Not Found"
- "BOOTMGR is missing"
- Pantalla negra post-BIOS

## Prerrequisitos

- USB de Windows: `Win_10_Pro_19045_4651` (Kingston DataTraveler 3.0, E:)
- Backup BCD: `C:\Backups\Boot\BCD-backup-*.bcd`

## Procedimiento

### A — Reparar sin perder datos

1. Conectar USB de Windows.
2. Reiniciar, F11, bootear desde USB.
3. En pantalla de instalación: "Repair your computer" → "Troubleshoot" → "Command Prompt".

4. Verificar que C: es correcta:
   ```
   diskpart
   list disk
   select disk 2
   list partition
   ```
   Confirmar: Part 1 = 477 GB, tipo Primary.

5. Marcar activa y reparar:
   ```
   select partition 1
   active
   exit
   bcdboot C:\Windows /s C: /f BIOS
   bootsect /nt60 C: /mbr
   ```

6. Reiniciar. Si arranca → listo.

### B — Si el BCD está corrupto

1. Renombrar BCD viejo:
   ```
   ren C:\Boot\BCD C:\Boot\BCD.bak
   ```
2. Recrear BCD:
   ```
   bcdboot C:\Windows /s C: /f BIOS
   ```

### C — Último recurso: restaurar BCD del backup

1. Desde el USB, copiar el backup al sistema:
   ```
   copy C:\Backups\Boot\BCD-backup-20260623-184256.bcd C:\Boot\BCD
   ```

### D — Si nada funciona: arrancar desde SSD viejo

1. El Disco 0 (SSD 250 GB) aún tiene el BCD original.
2. Entrar en BIOS (F2/Del) → Boot → Hard Drive BBS Priorities.
3. Poner el SSD de 250 GB como primer disco.
4. Guardar y reiniciar.
5. El sistema arranca con la configuración anterior.
