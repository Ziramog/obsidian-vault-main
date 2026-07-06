---
company: Wolfim
channel: Meta Ads
status: propuesta-no-publicada
created: 2026-07-06
owner: wolfim-growth
---

# Meta Ads — Reset hacia conversión real

## Diagnóstico

La campaña `CBA_PYMES_DUENOS_30-60` generó tráfico barato pero no negocio:

| Métrica | Resultado |
|---|---:|
| Visitas | 117 |
| Gasto | USD 4,77 |
| Costo por visita | USD 0,04 |
| Formularios reales en Supabase | 0 |
| Formularios de prueba | 1, propio |
| Conversión real | 0,00% |

Conclusión: **no escalar tráfico frío genérico a diagnóstico web**. La visita barata fue un falso positivo.

## Hipótesis nueva

Para convertir desde Meta, Wolfim necesita reducir fricción y aumentar especificidad:

1. No mandar frío genérico a una landing larga como primer paso.
2. Testear captación nativa dentro de Meta y WhatsApp directo.
3. Verticalizar el dolor: inmobiliarias/loteos/autos/PyMEs locales, no “PyMEs” genérico.
4. Usar la landing `/diagnostico` como respaldo o segunda etapa, no como único mecanismo.

## Estructura propuesta — 7 días

Presupuesto máximo sugerido: **USD 84 total / 7 días**.

| Experimento | Presupuesto | Objetivo | Métrica principal |
|---|---:|---|---|
| A. Lead Form nativo Meta | USD 5/día × 7 = USD 35 | Capturar nombre + web + WhatsApp sin salir de Instagram/Facebook | Costo por lead real |
| B. WhatsApp directo | USD 5/día × 7 = USD 35 | Generar conversación inmediata con Juan | Conversaciones calificadas |
| C. Retargeting visitantes | USD 2/día × 7 = USD 14 | Reimpactar visitas previas de wolfim.com/diagnostico | Leads o WhatsApps |

Una sola venta de USD 200 cubre 2,38 veces el test completo.

## Experimento A — Lead Form nativo

### Por qué
La campaña anterior pudo fallar por fricción post-click: salir de Meta, esperar carga, leer landing, completar formulario. El formulario nativo reduce esa fricción.

### Formulario
Campos:
- Nombre
- Sitio web o Instagram
- WhatsApp
- Rubro

Pregunta de calificación:
- “¿Qué querés mejorar?”
  - Recibir más consultas por WhatsApp
  - Mostrar mejor mis productos/propiedades
  - Renovar una web vieja
  - No estoy seguro

Mensaje de cierre:
> Perfecto. Juan de Wolfim revisa tu web/Instagram y te escribe por WhatsApp con 2 o 3 mejoras concretas.

### Copy base

**Texto principal:**
> Si tenés una empresa, inmobiliaria, loteo o negocio local, tu web/Instagram puede estar frenando consultas sin que te des cuenta.
>
> Te reviso la presencia digital y te marco 2 o 3 mejoras concretas.
>
> Sin cargo. Sin compromiso.

**Headline:**
> Pedí una revisión gratuita

**CTA Meta:**
> Registrarte / Más información

## Experimento B — WhatsApp directo

### Por qué
Wolfim vende con Juan como cara visible. Si la relación humana es el diferencial, WhatsApp puede superar al formulario.

### Mensaje prellenado
> Hola Juan, vi el anuncio de Wolfim. Quiero que revises mi web/Instagram y me digas qué se puede mejorar.

### Copy base

**Texto principal:**
> ¿Tu negocio depende de WhatsApp para vender?
>
> Entonces tu web o Instagram tiene que hacer una cosa rápido: generar confianza y llevar la consulta al lugar correcto.
>
> Escribime y te digo qué mejoraría en tu caso.

**Headline:**
> Revisamos tu web o Instagram

**CTA:**
> Enviar mensaje

## Experimento C — Retargeting

### Audiencia
Personas que visitaron:
- wolfim.com
- wolfim.com/diagnostico
- wolfim.com/inmobiliarias
- páginas de casos/portfolio

Ventana: 30-90 días según tamaño de audiencia.

### Copy
> Entraste a Wolfim pero quizás no pediste diagnóstico.
>
> Si querés, mandanos tu web o Instagram y te decimos qué mejorar para generar más consultas.

CTA: WhatsApp o formulario nativo.

## Creatividades

No usar imagen institucional genérica. Usar piezas por dolor concreto.

### Pieza 1 — checklist
```text
Tu web puede estar perdiendo consultas si:
☐ WhatsApp no se ve rápido
☐ El sitio carga lento en celular
☐ No muestra bien lo que vendés
☐ Parece desactualizada

Revisión gratuita por Wolfim
```

### Pieza 2 — negocio local
```text
¿Tu negocio recibe pocas consultas?
Quizás el problema no es el producto.
Quizás es cómo se ve online.

Te marcamos 3 mejoras concretas.
```

### Pieza 3 — vertical inmobiliaria/loteo
```text
Propiedades, lotes o desarrollos
necesitan algo más que posteos.

Mostralos con una página clara
+ WhatsApp directo.
```

## Criterios de decisión

| Resultado después de 7 días | Decisión |
|---|---|
| 5+ leads reales y al menos 1 calificado | Mantener ganador y pausar perdedores |
| 1-4 leads reales | Iterar copy/vertical, no escalar todavía |
| 0 leads | Pausar todo; Meta frío no está validado para este offer |
| Muchos mensajes basura | Subir fricción/calificación en copy |
| Leads buenos pero caros | Mejorar creatividad y segmentación, no abandonar canal todavía |

## Regla comercial

No volver a juzgar Meta por visitas. Desde ahora, la métrica de campaña es:

1. Leads reales
2. WhatsApps calificados
3. Reuniones/conversaciones con potencial
4. Ventas

Visitas, CTR y CPC solo sirven como diagnóstico secundario.

## No publicar sin aprobación

Este documento es propuesta. No activar campañas ni gastar presupuesto sin aprobación explícita de Juan.
