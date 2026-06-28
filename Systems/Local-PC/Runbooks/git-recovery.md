# Runbook: Recuperación de Git y Credenciales

## Verificación actual

```
gh auth status
git config --global user.name
git config --global user.email
```

## Si gh auth falla

```
gh auth login
# Elegir: GitHub.com → HTTPS → Login with web browser
gh auth setup-git
```

## Token ghp_ revocado

El token `ghp_` estaba embebido en `wolfim-web/.git/config`. Fue revocado el 2026-06-23.
El remote ahora es: `https://github.com/Ziramog/wolfim-web.git` (limpio, sin credenciales).

## Si un repo no tiene remote

```bash
# Verificar
git -C <repo> remote -v

# Agregar (ejemplo)
git -C <repo> remote add origin https://github.com/Ziramog/<repo-name>.git
```

## Si hay SID mismatch (dubious ownership)

```bash
# Por comando (no wildcard global)
git -c "safe.directory=<ruta>" -C <ruta> <comando>
```

## Repos y sus remotes (mapeo)

Ver `SYSTEM-INVENTORY.md` para la lista completa de 24 repos y sus remotes en GitHub.

## SSH vs HTTPS

Actualmente se usa **HTTPS** con token OAuth (`gho_`) almacenado en Windows keyring.
No hay claves SSH configuradas (sin `.ssh/`).
HTTPS es suficiente para operaciones normales.
