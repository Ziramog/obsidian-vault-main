---
company: ANGO
project: website
change: visual-level-up-option-b
status: implemented-local
implemented: 2026-07-12
repo: C:\Projects\ANGOWEB2\astro-site
---

# Level up visual — Modelos y Garantía

## Alcance

Se implementó directamente la opción B aprobada por Juan sobre dos secciones de la homepage:

- `Embragues industriales y tomas de fuerza (PTO) / Modelos y capacidades`
- `Nuestra garantía / Marca registrada`

## Approach

### Modelos

- Showcase técnico en grilla desktop 55/45.
- Fondo con grilla de ingeniería y frame rígido.
- Producto ampliado con callouts SAE, discos y torque.
- Jerarquía simplificada: kicker, categoría, título y descripción.
- Descarga del catálogo convertida en módulo técnico navy/dorado.
- Composición mobile específica y protección frente al WhatsApp FAB.

### Garantía RG

- Sección convertida en un cierre de marca dentro de un shell navy con borde dorado.
- Logo RG presentado como sello de origen.
- Resistencia, confianza y seguridad convertidas en módulos técnicos numerados.
- Producto RG ampliado sobre retícula y halo técnico.
- Caption de fabricación nacional y continuidad hacia el footer.

## Archivos modificados

- `src/components/Models.astro`
- `src/components/Brand.astro`

## Restricciones respetadas

No se modificaron hero, formulario, lógica de contacto, repuestos, navbar, footer, PDF ni assets originales.

## Verificación

- `npm run build`: exitoso; 2 páginas generadas.
- QA visual desktop: 1264 px.
- QA visual mobile real mediante emulación CDP: 390 × 844 px.
- Sin overflow horizontal a 390 px (`scrollWidth = viewport = 390`).
- Imágenes cargadas y sin errores de consola JavaScript.
- `git diff --check`: limpio.

## Pendiente

- Revisión visual final de Juan.
- Commit y deploy no realizados.
