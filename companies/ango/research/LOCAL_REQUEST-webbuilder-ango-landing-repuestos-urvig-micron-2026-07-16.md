---
type: LOCAL_REQUEST
status: ready-for-brain-vps-handoff
from: ango-commercial
to: brain-vps
requested-assignee: web-builder
company: ANGO
project: google-ads-2026-06
priority: high
created-at: 2026-07-16
approval-source: Juan
requires-local: true
---

# LOCAL_REQUEST — web-builder — landing ANGO repuestos Urvig/Micron

## Pedido de Juan

Juan pide armar una página dedicada para **repuestos compatibles Urvig/Micron** y usar la web actual de ANGO para **embragues RG / tomas de fuerza industriales**.

No es pedido para cambiar estrategia de negocio: es implementación web para campaña Google Ads ANGO.

## Contexto operativo

La campaña Google Ads definitiva ya quedó definida como:

```text
Campaña: ANGO | Search | Compatibles + RG | 2026
├── Grupo 1: Compatibles Urvig
├── Grupo 2: Compatibles Micron
└── Grupo 3: Productos RG / PTO Industrial
```

Documento base:

```text
companies/ango/projects/google-ads-2026-06/campana-definitiva-google-ads-ango-2026-07-16.md
```

Análisis de Keyword Planner:

```text
companies/ango/intelligence/google-ads-keyword-planner-2026-analisis.md
```

Contexto actualizado:

```text
companies/ango/intelligence/context.md
companies/ango/intelligence/patterns.md
```

## Captura de la web actual

Referencia visual guardada en el vault:

```text
companies/ango/research/assets/ango-web-current-home-2026-07-16.png
```

La web actual comunica muy bien productos RG/PTO industriales:

- hero de tomas de fuerza con embrague;
- producto RG visible;
- aplicaciones industriales;
- calculadora técnica;
- modelos y capacidades;
- catálogo técnico RG;
- garantía / marca registrada RG;
- contacto ANGO.

## Decisión de landing

Usar la web actual/home para:

```text
Grupo 3: Productos RG / PTO Industrial
```

Crear una página dedicada para:

```text
Grupo 1: Compatibles Urvig
Grupo 2: Compatibles Micron
```

URL sugerida:

```text
/repuestos-compatibles-urvig-micron
```

Alternativas aceptables:

```text
/repuestos-urvig-micron
/repuestos-compatibles
```

## Objetivo de la página

La página debe convertir búsquedas de alta intención como:

```text
repuestos urvig
repuestos compatibles urvig
repuesto embrague urvig
repuestos micron
repuestos compatibles micron
repuesto embrague micron
```

El usuario debe entender en 5 segundos:

1. ANGO ofrece repuestos compatibles para Urvig y Micron.
2. No son repuestos originales ni representación oficial.
3. Debe consultar compatibilidad por modelo o enviar foto.
4. Puede pedir precio/stock rápido por WhatsApp o formulario.

## Copy recomendado

### Hero

Título:

```text
Repuestos compatibles para Urvig y Micron
```

Subtítulo:

```text
Fabricación nacional y soluciones compatibles para mantenimiento de equipos industriales. Consultá disponibilidad según modelo.
```

CTAs:

```text
Consultar compatibilidad
Enviar foto del repuesto
Pedir precio por WhatsApp
```

### Bloque Urvig

Título:

```text
Compatibles para equipos Urvig
```

Texto:

```text
Repuestos compatibles para equipos Urvig. Asesoramiento técnico directo, fabricación nacional y envío a todo el país. Consultá por modelo, aplicación o foto del repuesto.
```

### Bloque Micron

Título:

```text
Compatibles para equipos Micron
```

Texto:

```text
Alternativas compatibles para equipos Micron. Revisamos modelo, medidas y aplicación para confirmar disponibilidad o fabricación.
```

### Bloque datos a pedir

Título:

```text
Qué necesitamos para cotizar
```

Campos o bullets:

```text
Marca del equipo: Urvig / Micron / otro
Modelo o placa del equipo
Foto del repuesto o embrague
Cantidad necesaria
Localidad / provincia
Teléfono o WhatsApp
```

Mensaje simple:

```text
Si no conoce el modelo, envíenos una foto y nuestro equipo revisa la compatibilidad.
```

### Aclaración legal/comercial

Incluir en sección baja o FAQ, no como freno en hero:

```text
Los nombres Urvig y Micron se utilizan únicamente para identificar compatibilidad. ANGO fabrica y comercializa soluciones compatibles; no se presenta como representante oficial salvo indicación expresa.
```

## Cambios recomendados en home actual

Si web-builder toca la home, corregir el bloque de repuestos para no confundir:

Actual observado en captura:

```text
Repuestos y reacondicionamiento
Repuestos línea RG
Repuestos Urvig y Micron
Compatibilidad total
repuestos originales
```

Recomendado:

```text
Repuestos y reacondicionamiento
Repuestos línea RG
Compatibles Urvig y Micron
Compatibilidad por modelo
repuestos fabricados por ANGO / repuestos línea RG
```

Evitar:

```text
original Urvig
original Micron
distribuidor oficial
service oficial
representante oficial
compatibilidad total
```

## Diseño esperado

Mantener identidad visual actual de ANGO:

- azul navy industrial;
- blanco técnico;
- acentos dorados;
- estética de ingeniería / plano técnico;
- producto grande, serio y mecánico;
- CTAs claros;
- mobile-first.

La landing puede reutilizar componentes visuales de la home, pero debe estar focalizada en repuestos compatibles, no en el discurso general de PTO.

## Requisitos técnicos mínimos

1. Página dedicada con URL estable.
2. SEO title y meta description orientados a repuestos compatibles Urvig/Micron.
3. H1 único con “Repuestos compatibles para Urvig y Micron”.
4. Botón WhatsApp visible en mobile.
5. Formulario corto o CTA a WhatsApp con campos/datos solicitados.
6. UTM compatible con Google Ads.
7. Cargar rápido en mobile.
8. No bloquear indexación salvo decisión contraria.
9. No afirmar representación oficial.

## Tracking recomendado

Preparar eventos o selectores para medir:

```text
whatsapp_clicked
phone_clicked
lead_form_submitted
email_clicked
```

Si no se implementa tracking en esta tarea, dejar IDs/classes claros para que luego se conecte GA4/Google Ads.

## Criterios de aceptación

- Existe página dedicada para repuestos compatibles Urvig/Micron.
- La home queda como destino válido para productos RG/PTO industriales.
- La landing no usa “original” ni “oficial” para Urvig/Micron.
- La landing pide modelo/foto/compatibilidad de forma clara.
- La landing funciona bien en mobile.
- Hay CTA directo a WhatsApp/teléfono/formulario.
- Se entrega URL de preview o producción.
- Se indica qué archivos/rutas se modificaron.

## Notas para brain-vps

Según directiva Sync V6, ango-commercial no debe hablar directo con web-builder. Este archivo es el brief `LOCAL_REQUEST` dentro de la zona ANGO para que brain-vps cree o valide el handoff oficial en:

```text
Hermes/Handoffs/vps-to-local/
```
