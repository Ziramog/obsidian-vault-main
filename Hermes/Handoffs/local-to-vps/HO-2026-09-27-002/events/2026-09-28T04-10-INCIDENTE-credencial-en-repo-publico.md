# INCIDENTE — credencial de la PC publicada en el repo PÚBLICO del vault

- **Detectado:** 2026-09-28 ~04:10 UTC (2026-09-28 ~00:10 -04:00) por brain-local
- **Severidad:** alta — exposición activa (el secreto está en el tip de un repo público)
- **Actor de la remediación parcial:** brain-local (sólo dentro de su zona de escritura)

## Qué se encontró

`github.com/Ziramog/obsidian-vault-main` es **PÚBLICO** (verificado sin autenticación:
`https://github.com/Ziramog/obsidian-vault-main` → 200 y
`https://api.github.com/repos/Ziramog/obsidian-vault-main` → 200; contraste:
`Ziramog/PWA-Hermes` → 404 en ambos, ése sí es privado).

El valor literal de `API_SERVER_KEY` de la **PC local** (21 caracteres, sha256
`24a07bb1…`) aparecía en el tip de ese repo público en **dos archivos**
(`git grep -lF <literal> origin/main`):

| Archivo | Estado |
|---|---|
| `Hermes/Handoffs/local-to-vps/HO-2026-09-27-002/events/2026-09-28T00-34-pwa-pusheada-deploy-base.md` | **redactado** por brain-local (worktree); pendiente de push por el sync |
| `hq/sessions/2026-09-27.md` | **sin tocar** — fuera de la zona de escritura de brain-local |

Además, ese mismo valor es el literal versionado en `PWA-Hermes/README.md:31` (repo
privado) y está presente en los 9 `.env` de los perfiles de la PC.

## Causa raíz del error de razonamiento

El evento que lo publicó afirma *"Está en un repo privado y en el historial"*. La frase
mezcla dos repos: **`PWA-Hermes` es privado, el vault es público**. La premisa de
privacidad del vault nunca se verificó y es la que autorizó escribir el valor en un
archivo que sincroniza a GitHub cada 2 minutos.

## Remediación aplicada (brain-local)

- El literal se reemplazó por `[credencial: API_SERVER_KEY]` en el evento de la zona
  propia: `grep -cF <literal>` sobre el archivo pasó de **1 → 0**.
- Se corrigió la frase de la premisa falsa en ese evento.
- Este acta documenta el incidente y lo pendiente.

## Pendiente (requiere decisión de Juan — no se tocó)

1. **Rotar la `API_SERVER_KEY` de la PC.** El valor está quemado en un repo público:
   hay que sacarlo de servicio, no sólo redactarlo. Ojo que rotarlo en la PC sola deja
   el 401 cruzado con el VPS: conviene rotar y **unificar** el valor de ambos nodos en
   la misma pasada.
2. **`hq/sessions/2026-09-27.md`** — mismo tratamiento, pero el archivo no es de
   brain-local: redactar ahí también (la redacción sólo lo saca del *tip*).
3. **Historial.** El valor vive en los commits `1c3f5ff2` y `f91b4d04`, así que
   redactar el tip **no lo borra**. Dos caminos: hacer privado el vault (un click,
   elimina el acceso) o reescribir el historial con force-push.
4. **Auditoría más amplia.** Un barrido por patrones de nombres de credencial sobre el
   tip (`API_SERVER_KEY|TELEGRAM_BOT_TOKEN|*_API_KEY|ghp_…|sk-…`) devuelve 17 archivos;
   la mayoría son **menciones por nombre, no valores**, pero merece una revisión
   dedicada antes de afirmar que el vault está limpio. No se revisó valor por valor.
