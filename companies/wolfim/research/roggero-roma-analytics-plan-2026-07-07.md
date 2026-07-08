---
title: Roggero & Roma — Plan de reporte Analytics primer mes
type: client-retention-plan
client: Roggero & Roma
contact: Franco Roma
site: https://www.roggeroyroma.com
owner: wolfim-growth
created: 2026-07-07
report-target: 2026-07-28
status: draft
---

# Roggero & Roma — Plan de reporte Analytics primer mes

## Contexto verificado

- Cliente: **Roggero & Roma / Franco Roma**.
- Sitio: **https://www.roggeroyroma.com**.
- Vertical: inmobiliaria, Alta Gracia / Córdoba.
- Caso Wolfim: sitio en producción, catálogo inmobiliario, panel de propiedades, Google Reviews, mapa/CTA.
- Analytics: el sitio en vivo tiene tag GA4 detectado el **2026-07-07**: `G-PW4FH9WHQB`.
- Agenda indica **Google Analytics Roggero & Roma implementado el 2026-06-28**.
- Primer corte de 30 días: **2026-07-28**.

## Objetivo comercial del reporte

No mostrar “métricas por métricas”. Mostrar que Wolfim le dio a Franco un activo medible:

1. Cuánta gente entra al sitio.
2. Desde dónde llega.
3. Qué propiedades o secciones generan más interés.
4. Cuántos intentos de contacto produce el sitio.
5. Qué ajustes concretos conviene hacer el próximo mes para generar más consultas.

**Mensaje central para Franco:**

> “Ya no estamos a ciegas. En el primer mes podemos ver qué mira la gente, desde dónde llega y qué conviene ajustar para que el sitio trabaje mejor como herramienta comercial.”

## Formato recomendado de entrega

### Entregable principal

**PDF corto de 3 a 5 páginas**, no un informe técnico largo.

1. Portada: “Primer mes de medición — Roggero & Roma”.
2. Resumen ejecutivo con 4 números grandes.
3. Interés de usuarios: páginas/propiedades más vistas.
4. Contactos e intención comercial: WhatsApp, formularios, teléfono/email si están trackeados.
5. Próximas acciones recomendadas.

### Presentación

- Ideal: **reunión / llamada de 10 a 15 min** con Franco.
- Alternativa: WhatsApp con PDF + audio corto de Juan explicando 3 puntos.
- No mandar capturas sueltas de GA4 sin interpretación: eso baja valor percibido.

## KPIs principales a mostrar

| Bloque | Métrica | Para qué sirve | Fuente |
|---|---|---|---|
| Alcance | Usuarios / sesiones | Tamaño real de audiencia del sitio | GA4 |
| Alcance | Vistas totales | Volumen de navegación | GA4 |
| Dispositivo | % mobile vs desktop | Priorizar UX mobile si domina celular | GA4 |
| Fuentes | Direct / Google / redes / referidos | Saber de dónde llega la demanda | GA4 adquisición |
| Interés | Top páginas / top propiedades | Saber qué propiedades atraen más | GA4 pages/screens |
| Intención | Clicks a WhatsApp | Señal comercial más importante | GA4 evento |
| Intención | Envíos de formulario | Lead directo | GA4 evento |
| Intención | Clicks teléfono/email | Contacto alternativo | GA4 evento |
| SEO | Consultas, impresiones, clicks | Ver si Google empieza a mostrar el sitio | Search Console, si está conectado |
| Operativo | Uptime / backup realizado | Justificar mantenimiento y confianza | Wolfim interno |

## Eventos que conviene tener trackeados antes del corte

Si hoy solo está cargado GA4 básico, el reporte va a mostrar visitas pero no intención comercial. Para que el informe cierre mejor, conviene verificar o implementar estos eventos:

| Evento GA4 | Trigger | Propiedades útiles | Prioridad |
|---|---|---|---|
| `property_viewed` | Usuario abre ficha de propiedad | `property_id`, `property_title`, `operation`, `property_type`, `location` | 🔴 Alta |
| `whatsapp_clicked` | Click en WhatsApp general o por propiedad | `location`, `property_id`, `page_path` | 🔴 Alta |
| `contact_form_submitted` | Formulario enviado | `form_name`, `page_path` | 🔴 Alta |
| `phone_clicked` | Click en teléfono | `location`, `page_path` | 🟡 Media |
| `email_clicked` | Click en email | `location`, `page_path` | 🟡 Media |
| `search_used` | Uso de buscador/filtros | `query`, `operation`, `property_type`, `location` | 🟡 Media |
| `map_interacted` | Click/uso de mapa | `page_path`, `property_id` | 🟢 Opcional |

**Regla:** no enviar datos personales a GA4. Nada de nombres, teléfonos, emails ni mensajes del lead.

## Estructura del PDF mensual

### Página 1 — Resumen ejecutivo

Título: **Primer mes de medición: cómo está funcionando el sitio**

Cuatro tarjetas grandes:

- Visitas / usuarios.
- Páginas vistas.
- Propiedades más consultadas.
- Contactos generados o intentos de contacto.

Texto breve:

> “Este primer mes funciona como línea base. A partir de ahora podemos comparar mes contra mes y tomar decisiones con datos reales.”

### Página 2 — De dónde llega la gente

Mostrar:

- Google orgánico.
- Directo.
- Redes sociales.
- Referidos.
- Campañas pagas si existieran.

Interpretación que busca Franco:

- Si Google orgánico empieza a aparecer: “El sitio ya puede captar demanda propia”.
- Si domina directo: “La marca ya se está buscando / compartiendo”.
- Si redes lleva tráfico: “Conviene empujar propiedades destacadas desde Instagram/WhatsApp”.

### Página 3 — Qué mira la gente

Mostrar top páginas o propiedades:

| Ranking | Página / propiedad | Vistas | Lectura comercial |
|---|---|---:|---|
| 1 | [propiedad] | [dato] | Interés alto |
| 2 | [propiedad] | [dato] | Usar en difusión |
| 3 | [propiedad] | [dato] | Revisar CTA |

Interpretación:

- Qué tipo de inmueble tracciona.
- Qué propiedades conviene publicar más.
- Qué páginas reciben visitas pero no contacto.

### Página 4 — Contactos e intención comercial

Mostrar:

- Clicks a WhatsApp.
- Formularios enviados.
- Clicks a teléfono/email.
- Tasa simple: contactos / sesiones.

Si no hay eventos suficientes:

> “Este mes ya medimos tráfico. Para el próximo corte recomendamos medir clicks a WhatsApp por propiedad para saber qué inmuebles generan consultas reales.”

### Página 5 — Próximas acciones

No cerrar con “métricas”. Cerrar con acciones:

| Prioridad | Acción | Por qué |
|---|---|---|
| 🔴 | Medir WhatsApp por propiedad | Saber qué inmueble genera consulta real |
| 🟡 | Reforzar propiedades más vistas en redes | Aprovechar interés ya detectado |
| 🟡 | Mejorar buscador/filtros si hay búsquedas sin conversión | Convertir navegación en contacto |
| 🟢 | Conectar Search Console si no está | Medir crecimiento SEO local |

## Talk track para Juan

> “Franco, esto no es solo para ver visitas. La idea es que el sitio empiece a trabajar como una herramienta comercial medible. En este primer mes ya podemos ver cuánta gente entra, qué secciones mira y desde dónde llega. Lo importante es que ahora tenemos línea base: el mes que viene podemos comparar y saber qué mejora.”

> “El punto fuerte no es mirar Google Analytics todos los días. El punto fuerte es tomar 2 o 3 decisiones concretas por mes: qué propiedad empujar, dónde mejorar el contacto y qué sección del sitio está funcionando mejor.”

## WhatsApp breve para enviar antes del reporte

> Franco, ¿cómo va? Ya tenemos Analytics funcionando en el sitio. A fin de mes te preparo un resumen simple del primer mes: visitas, de dónde llega la gente, qué propiedades/secciones miran más y qué ajustes conviene hacer para generar más consultas. No va a ser un informe técnico largo, sino algo práctico para tomar decisiones.

## Upsells naturales según lo que muestre Analytics

| Señal en datos | Oportunidad comercial |
|---|---|
| Muchas visitas pero pocos contactos | Optimización de CTAs / WhatsApp por propiedad |
| Varias búsquedas internas | Mejorar buscador y filtros, item ya pendiente en reformas |
| Propiedades específicas muy vistas | Paquete de difusión / PDF comparativo / publicación destacada |
| Google orgánico empieza a traer tráfico | SEO local mensual o carga optimizada de propiedades |
| Mobile domina el tráfico | Mejora de cards, velocidad y contacto mobile |

## Checklist operativo

| Fecha | Acción | Responsable |
|---|---|---|
| 2026-07-07 | Confirmar acceso de Juan a GA4 y propiedad `G-PW4FH9WHQB` | Juan / Wolfim |
| Esta semana | Verificar si existen eventos de WhatsApp/formulario/property view | Wolfim |
| Esta semana | Si faltan, pedir a web-builder implementación mínima de eventos | brain-vps → local |
| 2026-07-15 | Chequeo intermedio: confirmar que entran datos y eventos | Wolfim |
| 2026-07-28 | Extraer datos del primer corte de 30 días | Wolfim |
| 2026-07-28/29 | Preparar PDF corto + guion de explicación | Wolfim |
| Después del envío | Proponer 2 acciones de mejora para agosto | Juan / Wolfim |

## Decisiones pendientes para Juan

1. Confirmar si ya tiene acceso a la propiedad GA4 o si hay que recuperarlo.
2. Confirmar si quiere PDF formal o WhatsApp + captura interpretada.
3. Confirmar si se puede agregar medición de clicks a WhatsApp antes del 28/07.
4. Confirmar si Search Console está conectado al dominio.

## Criterio de éxito

El reporte es bueno si Franco entiende en menos de 5 minutos:

1. “Mi sitio recibe tráfico real.”
2. “Puedo saber qué propiedades interesan.”
3. “Wolfim no solo hizo la web: la mide y propone mejoras.”
4. “Tiene sentido mantener el servicio activo.”
