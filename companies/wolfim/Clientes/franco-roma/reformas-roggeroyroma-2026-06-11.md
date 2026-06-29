---
title: Reformas Roggeroyroma — semana 11/06
type: reformas
status: pending
fuente: chat 2026-06-11
sitio: roggeroyroma.com
---

# Reformas pendientes — roggeroyroma.com
> Anotado 11/06 vía chat · 3 ítems para esta semana

## 1. Search bar — mejorar sintaxis de búsqueda
- [ ] Revisar lógica actual del buscador de propiedades
- [ ] Definir mejoras: ¿tolerancia a typos? ¿búsqueda por código? ¿filtros combinados?
- [ ] Implementar y testear

## 2. Retorno de carga de propiedad
- [ ] Al cargar/guardar una propiedad, volver a la **sección relativa** a esa propiedad (no al top de la página)
- [ ] Comportamiento esperado: scroll/anchor al item guardado, o highlight temporal

## 3. Etiqueta "EXCELENTE PRECIO" + temporizador
- [ ] Agregar etiqueta visual especial **"EXCELENTE PRECIO"** en propiedades marcadas
- [ ] Comportamiento temporizador:
  - Etiqueta aparece en propiedades **nuevas** (definir criterio: ¿recién cargadas? ¿precio destacado al alta?)
  - Después de **3 meses** desde la carga → reemplazar automáticamente por **"xxxxx"**
- [ ] Definir: ¿"xxxxx" literal? ¿Etiqueta vacía? ¿Otro placeholder? (confirmar con Juan)
- [ ] Job/cron para el reemplazo automático o ¿se evalúa en cada render?

## 4. Recordatorio mods — Revver sup. cubierta exterior e interior + ícono
- [ ] Agregar recordatorio en mods para **Revver** (recordatorio al usuario/admin)
- [ ] Cubre **sup. cubierta exterior e interior**
- [ ] Mostrar con **ícono** (definir cuál)

---

## 🧠 Notas
- Sitio en producción (cliente Franco Roma — mantenimiento anual $250 ya cobrado)
- Cambios son técnicos de front/admin · no afectan contenido comercial inmediato
- **Pendiente definir antes de implementar:**
  - Item 1: alcance concreto de "mejorar sintaxis"
  - Item 3: significado exacto de "xxxxx" (vacío / literal / reemplazo visual)
