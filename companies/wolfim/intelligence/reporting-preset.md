---
title: Wolfim — Preset profesional para informes PDF
owner: wolfim-growth
type: reporting-preset
created: 2026-07-07
status: active
script: /home/hermes/scripts/wolfim_report_preset.py
brand-assets:
  logo-black: companies/wolfim/brand/wolfim_logo_black.svg
  logo-white: companies/wolfim/brand/wolfim_logo_white.svg
  isologo-black: companies/wolfim/brand/wolfim_isologo_black.svg
  isologo-white: companies/wolfim/brand/wolfim_isologo_white.svg
---

# Wolfim — Preset profesional para informes PDF

## Objetivo

Estandarizar los informes comerciales de Wolfim para que cualquier reporte tenga:

- portada profesional,
- logo de Wolfim visible,
- estructura clara para cliente,
- métricas convertidas en lectura comercial,
- footer consistente con isologo,
- cierre con próximo paso accionable.

## Implementación activa

Script reutilizable de ejecución en VPS:

`/home/hermes/scripts/wolfim_report_preset.py`

Copia versionada en vault para reuso/sync:

`/home/hermes/obsidian-vault/companies/wolfim/intelligence/wolfim_report_preset.py`

Generador aplicado a Roggero & Roma:

`/home/hermes/scripts/generate_roggero_analytics_mensual_wolfim.py`

PDF generado:

`/home/hermes/Transfer-files/roggero_roma_informe_mensual_analytics_wolfim_2026-07-07.pdf`

## Assets de marca

| Uso | Asset | Estado |
|---|---|---|
| Logo horizontal negro | `companies/wolfim/brand/wolfim_logo_black.svg` + `.png` | Activo / transparente |
| Logo horizontal blanco | `companies/wolfim/brand/wolfim_logo_white.svg` + `.png` | Activo / transparente |
| Isologo negro | `companies/wolfim/brand/wolfim_isologo_black.svg` + `.png` | Activo / transparente |
| Isologo blanco | `companies/wolfim/brand/wolfim_isologo_white.svg` + `.png` | Activo / transparente |

El preset prefiere PNG transparente para compatibilidad con `fpdf2` y conserva SVG como fuente escalable. En fondos claros usa logo/isologo negro; en cierre oscuro usa isologo blanco.

## Sistema visual

| Token | Valor | Uso |
|---|---|---|
| Ink | `#0A0A0F` | Títulos, headers de tabla, cierre |
| Red | `#E61E1E` | Línea de acento, barras laterales, alertas |
| Soft | `#F7F8FA` | Cards y fondos suaves |
| Line | `#DEE2EA` | Separadores |
| Text | `#24272E` | Texto principal |
| Muted | `#5D6574` | Notas, subtítulos, captions |

Tipografía operativa: DejaVu Sans como fallback estable en VPS. Visualmente cumple rol de sans limpia tipo Inter y soporta acentos.

## Estructura estándar del informe

1. **Portada**
   - Logo Wolfim arriba izquierda.
   - Pill “INFORME WOLFIM” arriba derecha.
   - Título grande.
   - Subtítulo explicativo.
   - Card con cliente, período, destinatario y fecha.
   - Frase de intención: “convertir datos en decisiones comerciales”.

2. **Resumen ejecutivo**
   - No listar datos sueltos.
   - Abrir con la lectura comercial principal.
   - Usar 4–6 métricas máximas en cards.

3. **Bloque de lectura clave**
   - Callout verde para conclusión positiva.
   - Callout rojo/suave para aclaración importante.

4. **Tabla de datos**
   - Encabezado negro.
   - Filas alternadas suaves.
   - Columnas con lectura, no solo números.

5. **Señales comerciales**
   - Bullets accionables.
   - En idioma de negocio, no técnico.

6. **Próximo paso recomendado**
   - Una recomendación clara.
   - Evitar terminar con diagnóstico sin acción.

7. **Cierre Wolfim**
   - Panel oscuro con isologo.
   - Mensaje de valor: el sitio como herramienta comercial medible.

## Reglas de redacción para informes Wolfim

- Decir “procedencia estimada” en vez de “nacionalidad”.
- No exponer problemas internos de tracking salvo que sea necesario.
- No vender humo con usuarios internacionales si no tienen profundidad.
- Siempre explicar el número con una lectura comercial.
- No usar “preliminar” si el período ya cubre 30 días.
- Cerrar con próximo paso medible.

## Uso técnico

```python
import sys
sys.path.append('/home/hermes/scripts')
from wolfim_report_preset import WolfimReport, copy_to_transfer

pdf = WolfimReport(
    report_title='Informe mensual de Analytics',
    client_name='Cliente',
    footer_text='Wolfim Studio · Medición web y crecimiento comercial',
)

pdf.add_cover(
    title='Informe mensual de Analytics',
    subtitle='Lectura comercial del rendimiento web.',
    client='Cliente',
    period='Últimos 30 días',
    prepared_for='Contacto',
    date_label='DD/MM/YYYY',
)

pdf.add_page()
pdf.section('Resumen ejecutivo', 'Lectura comercial')
pdf.body('Texto ejecutivo...')
pdf.metric_cards([
    ('Usuarios activos', '293', 'últimos 30 días'),
    ('Sesiones', '520', 'visitas al sitio'),
])
pdf.callout('Conclusión principal', 'Texto...', tone='green')
pdf.table(['Columna', 'Dato'], [['Ejemplo', '123']], [89, 89])
pdf.closing_panel('Cierre Wolfim', 'Próximo paso...')

out = '/home/hermes/reporte.pdf'
pdf.output(out)
copy_to_transfer(out)
```

## Validación visual

El PDF de Roggero & Roma fue generado y renderizado a imágenes para revisar portada y páginas internas. Versión actual validada con el pack transparente 2026-07-08: logo negro en portada/header, isologo negro en footer y portada, isologo blanco en el panel de cierre.
