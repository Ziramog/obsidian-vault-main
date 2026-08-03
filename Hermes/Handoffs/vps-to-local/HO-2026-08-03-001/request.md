---
id: HO-2026-08-03-001
status: ready
from: brain-vps
to: brain-local
project: almas-libres
priority: normal
depends-on: []
created-at: 2026-08-03T10:28:37-03:00
acknowledge-by: next-local-session
due-at: 2026-08-07T18:00:00-03:00
escalate-after: 96h
briefing: Hermes/Briefings/current.md
director: Juan
---

# Handoff — web-builder — MVP web Fundación Almas Libres + padrinazgo equino

## Autorización y alcance

Juan autorizó explícitamente este delivery puntual durante la sesión del 2026-08-03. El briefing global está vencido y Wolfim continúa siendo la prioridad general; este handoff no cambia ese foco.

La tarea es construir una primera versión verificable de la web de Fundación Almas Libres, orientada a:

1. generar confianza;
2. explicar el trabajo de la Fundación;
3. convertir interés en padrinazgos y otras formas de ayuda;
4. preparar una base mantenible para incorporar fotos y datos reales de los caballos.

La primera entrega debe quedar en **preview**, no publicada como sitio oficial hasta completar la validación institucional y los datos bloqueantes listados en este documento.

## Objetivo verificable

Entregar un MVP responsive y navegable con:

- home institucional completa;
- experiencia dedicada de **“Apadriná un caballo”**;
- grilla data-driven preparada para al menos 6 caballos;
- CTA de contacto configurable, preferentemente vía WhatsApp;
- contenido cálido, sobrio y directo;
- secciones de ayuda, transparencia, preguntas frecuentes y contacto;
- build, lint/typecheck y pruebas básicas aprobadas;
- preview HTTP verificable en desktop y mobile;
- ningún dato inventado presentado como real.

## Contexto institucional confirmado

- Nombre: **Fundación Almas Libres**.
- Actividad: santuario equino y cuidado de caballos asilvestrados.
- Escala aproximada conocida: alrededor de 50 caballos; validar con Anne/Magalí antes de publicar la cifra.
- Anne: presidenta; aprueba voz institucional, campañas y alianzas sensibles.
- Magalí: vicepresidenta; valida operación y necesidades reales del santuario.
- Juan: implementación digital.
- Objetivo digital inicial: confianza + recaudación recurrente, no diseño perfecto.
- Estilo: español argentino, cálido, sobrio y directo. Emoción con transparencia; nunca morbo ni manipulación con culpa.

Fuente operativa a leer:

```text
/home/hermes/almas-libres/AGENTS.md
```

## Estado actual

En el VPS no existe todavía un proyecto web ni un banco de imágenes para Almas Libres. El workspace solo contiene `AGENTS.md`.

Antes de crear o modificar código, web-builder debe:

1. buscar en el entorno local si ya existe repo/proyecto de Almas Libres;
2. conservar el stack y convenciones si existe;
3. si no existe, crear un proyecto nuevo dentro de la zona local de ownership de web-builder;
4. informar en `response.md` la ruta absoluta del proyecto usado;
5. no escribir código ni activos dentro del vault compartido.

## Deliverables obligatorios

### 1. Home `/`

Debe incluir, en este orden:

1. header y navegación;
2. hero;
3. franja breve de confianza;
4. qué hacemos;
5. bloque destacado de padrinazgo;
6. cómo funciona el padrinazgo;
7. otras formas de ayudar;
8. necesidad actual, preparada pero oculta hasta tener datos reales;
9. transparencia;
10. quiénes somos;
11. sponsors y aliados;
12. preguntas frecuentes;
13. contacto y footer.

### 2. Página `/apadrinar`

Debe incluir:

1. hero específico;
2. explicación clara del padrinazgo;
3. aclaración de que no implica propiedad ni adopción;
4. grilla de caballos;
5. detalle accesible por tarjeta, mediante modal/drawer o ruta individual;
6. explicación de cómo sumarse;
7. preguntas frecuentes específicas;
8. CTA final de contacto.

### 3. Modelo de datos de caballos

La grilla no debe construirse con componentes duplicados. Debe surgir de un único archivo de datos o fuente equivalente.

Modelo mínimo recomendado:

```ts
type Horse = {
  id: string
  slug: string
  name: string
  photo: string
  alt: string
  shortDescription: string
  extendedDescription?: string
  status: 'available' | 'paused' | 'hidden'
  featured?: boolean
  displayOrder: number
  draft: boolean
}
```

Reglas:

- los nombres reales deben ser confirmados;
- `draft: true` nunca debe publicarse como ficha real;
- no inventar edad, sexo, diagnóstico, rescate, temperamento ni historia;
- no afirmar exclusividad del padrinazgo;
- el sistema debe tolerar varios padrinos por caballo salvo decisión institucional posterior;
- debe ser fácil agregar, ocultar o reordenar caballos sin tocar el layout.

## Arquitectura de navegación

### Header

- logo o wordmark “Fundación Almas Libres”;
- enlaces: `La Fundación`, `Qué hacemos`, `Apadrinar`, `Cómo ayudar`, `Transparencia`, `Contacto`;
- CTA destacado: **Quiero ayudar**;
- menú mobile accesible.

### Comportamiento

- en la home, la navegación puede usar anclas;
- `Apadrinar` debe abrir `/apadrinar`;
- los CTA principales deben conducir a una acción real o a una indicación explícita de dato pendiente en preview;
- no dejar botones muertos.

## Copy base de la home

Este copy es borrador operativo. Anne debe aprobar la voz final antes de publicación.

### Hero

**Eyebrow:**

> Fundación Almas Libres

**Título:**

> Un lugar para vivir con cuidado y libertad

**Bajada:**

> Sostenemos un espacio donde caballos asilvestrados reciben alimento, cuidado y acompañamiento responsable. Tu ayuda puede transformarse en bienestar concreto.

**CTA primario:**

> Apadriná un caballo

**CTA secundario:**

> Conocé lo que hacemos

**Imagen:**

Usar una fotografía real y digna de la manada cuando esté disponible. Mientras tanto, usar un placeholder local claramente identificado como preview. No descargar una foto genérica de internet para simular material institucional.

### Franja de confianza

Usar tres conceptos, sin métricas inventadas:

- Cuidado responsable
- Ayuda concreta
- Transparencia

### Sección “Qué hacemos”

**Título:**

> Cuidar también es sostener todos los días

**Introducción:**

> El bienestar de los caballos depende de una red capaz de acompañar necesidades concretas con continuidad y responsabilidad.

**Bloques:**

1. **Alimentación y sostén diario**
   Acompañamos las necesidades de alimentación y cuidado cotidiano de la manada.

2. **Cuidado y asistencia**
   Observamos necesidades y gestionamos asistencia cuando corresponde, sin prometer servicios veterinarios propios que no estén confirmados.

3. **Bienestar y espacio**
   Trabajamos para sostener un entorno seguro y respetuoso para los caballos.

4. **Construcción del santuario**
   Cada aporte fortalece una base más estable para cuidar y proyectar el santuario en el tiempo.

### Sección destacada “Apadriná un caballo”

**Título:**

> Apadriná un caballo, acompañá una vida real

**Texto:**

> Con tu padrinazgo ayudás a sostener alimento, asistencia y bienestar para los caballos que viven bajo protección en Almas Libres. No se trata de una ayuda abstracta: se trata de acompañar vidas reales con un aporte estable, humano y transparente.

**Aclaración visible:**

> Apadrinar no implica propiedad ni adopción. Es una forma de acompañar económicamente el cuidado general de los caballos del santuario.

**CTA:**

> Conocer los caballos

Mostrar 3 fichas destacadas si existen caballos reales publicados; si no, mostrar un bloque editorial sin nombres ficticios.

### Sección “Cómo funciona”

1. **Conocé los caballos**
   Explorá las fichas disponibles y elegí cuál querés acompañar.

2. **Contactanos**
   Contanos a quién querés apadrinar y te explicamos las opciones vigentes.

3. **Sumate al cuidado**
   Tu aporte mensual ayuda a sostener las necesidades generales del santuario.

No prometer actualizaciones personalizadas ni periodicidad hasta que Anne/Magalí confirmen qué pueden sostener.

### Sección “Otras formas de ayudar”

**Título:**

> Hay distintas maneras de ser parte

**Opciones:**

- **Donación única** — Para transformar una ayuda puntual en cuidado concreto.
- **Socio/a mensual** — Para sostener el trabajo de la Fundación con mayor previsibilidad.
- **Sponsor empresa** — Para comercios, profesionales y empresas que quieran acompañar la causa.
- **Donación en especie** — Alimento, insumos, servicios o logística, siempre coordinados previamente.

Cada opción debe tener un CTA configurable. No integrar pagos ni publicar cuentas bancarias sin aprobación y datos reales.

### Sección “Necesidad actual”

Preparar el componente, pero mantenerlo oculto en producción mientras no haya información confirmada.

Debe admitir:

- título de campaña;
- descripción;
- objetivo real;
- fecha de actualización;
- CTA;
- progreso opcional solo si existen monto objetivo y monto recibido verificables.

Nunca mostrar barras o porcentajes ficticios.

### Sección “Transparencia”

**Título:**

> La confianza también se construye mostrando

**Texto:**

> Queremos que cada persona sepa qué necesidad está ayudando a cubrir. Esta sección reunirá prioridades vigentes, uso general de los aportes y reportes de la Fundación a medida que sean aprobados para publicación.

En preview, puede incluir tarjetas preparadas para:

- necesidades del mes;
- destino general de los aportes;
- reportes descargables.

No mostrar documentos simulados ni cifras ficticias.

### Sección “Quiénes somos”

**Título:**

> Una fundación dedicada al cuidado y al respeto

**Texto base:**

> Fundación Almas Libres trabaja para sostener un espacio de cuidado para caballos y construir una red de personas, profesionales, comercios y empresas comprometidas con esta causa.

La publicación de nombres, cargos, fotos y datos legales del equipo requiere aprobación de Anne.

### Sección “Sponsors y aliados”

**Título:**

> Una red que hace posible el cuidado

**Estado inicial si no hay logos aprobados:**

> Estamos construyendo una red local de personas, comercios y empresas que quieran acompañar esta causa.

No usar logos sin autorización.

### Preguntas frecuentes de la home

1. **¿Qué significa apadrinar un caballo?**
   Es realizar un aporte periódico para acompañar el cuidado general de los caballos del santuario.

2. **¿El caballo pasa a ser mío?**
   No. El padrinazgo no implica propiedad, adopción ni derechos sobre el animal.

3. **¿Mi aporte se usa únicamente para ese caballo?**
   El vínculo es simbólico y cercano, pero el aporte ayuda a sostener las necesidades generales del santuario y de la manada.

4. **¿Puedo realizar una donación única?**
   Sí. La Fundación podrá informar las formas vigentes una vez validado el canal de contacto y pago.

5. **¿Puedo colaborar como empresa?**
   Sí. Se puede conversar una modalidad de sponsor, donación en especie o colaboración profesional.

6. **¿Se puede visitar el santuario?**
   Las visitas, si están habilitadas, se coordinan previamente y dependen del bienestar de los animales, la seguridad y la capacidad operativa. No publicar dirección ni mapa.

### Contacto

**Título:**

> ¿Querés ayudar o necesitás más información?

**Texto:**

> Escribinos y te contamos cuáles son las formas de colaboración disponibles en este momento.

CTA principal configurable:

> Hablar por WhatsApp

CTA secundario configurable:

> Enviar un email

## Copy y estructura de `/apadrinar`

### Hero

**Título:**

> Apadriná un caballo

**Bajada:**

> Elegí una vida para acompañar y convertí tu aporte mensual en alimento, cuidado y sostén para toda la manada.

**Aclaración:**

> El padrinazgo es simbólico y no exclusivo. No implica propiedad ni adopción. Los aportes se destinan al cuidado general del santuario.

No publicar “no exclusivo” como decisión definitiva si Anne prefiere otro modelo; dejarlo configurable desde contenido.

### Introducción de grilla

**Título:**

> Conocé algunas de las vidas que hoy acompañamos

**Texto:**

> Cada ficha representa una forma de acercarte a la causa. Podés elegir un caballo para acompañar y sumar tu ayuda al cuidado general del santuario.

### Tarjeta de caballo

Cada tarjeta debe incluir:

- foto vertical o 4:3 consistente;
- nombre confirmado;
- descripción de 1 a 2 líneas;
- estado público si corresponde;
- CTA **Apadrinar**;
- link o acción **Conocer más**;
- disclaimer breve cerca de la grilla, no repetido de forma invasiva en todas las tarjetas.

### Seis registros de maqueta

Crear seis registros draft para probar el layout, pero no publicarlos como caballos reales:

1. `horse-01` — `[Nombre a confirmar]`
2. `horse-02` — `[Nombre a confirmar]`
3. `horse-03` — `[Nombre a confirmar]`
4. `horse-04` — `[Nombre a confirmar]`
5. `horse-05` — `[Nombre a confirmar]`
6. `horse-06` — `[Nombre a confirmar]`

Usar placeholders visuales locales diferentes para comprobar el layout. Las descripciones pueden tomar estas seis estructuras, siempre marcadas como borrador:

1. “Parte de las vidas que hoy cuidamos con compromiso y constancia.”
2. “Una presencia dentro de la manada, acompañada con respeto y cuidado.”
3. “Una de las vidas que encuentran protección y libertad posible en Almas Libres.”
4. “Cada caballo necesita una red que lo sostenga con responsabilidad.”
5. “Acompañar esta vida es también fortalecer la construcción del santuario.”
6. “Tu padrinazgo transforma sensibilidad en ayuda concreta.”

No usar los nombres ilustrativos “Luna”, “Mora”, “Tordo”, “India”, “Niebla” o “Sol” como si fueran reales.

### Detalle de caballo

Al abrir una ficha, mostrar:

- foto;
- nombre;
- descripción confirmada;
- qué significa acompañarlo;
- recordatorio de que el aporte sostiene el cuidado general;
- CTA de WhatsApp con el caballo preseleccionado;
- cierre accesible y navegación por teclado.

No mostrar edad, sexo, historial médico, origen o historia de rescate si no hay datos confirmados y autorización.

## CTAs y contacto

### WhatsApp recomendado para el MVP

Centralizar el número en una configuración única, por ejemplo:

```text
NEXT_PUBLIC_ALMAS_WHATSAPP_NUMBER
```

Comportamiento:

- si existe número validado, abrir WhatsApp con texto prellenado;
- ejemplo de mensaje: “Hola, quiero recibir información para apadrinar a [nombre confirmado].”;
- si no existe número, el CTA debe quedar claramente deshabilitado en preview con el texto “Canal de contacto pendiente de confirmación”;
- no usar un número personal por suposición;
- no guardar PII en frontend, logs o analytics.

### Donaciones

Preparar una configuración para `donationUrl`, pero no integrar pasarelas, alias, CBU ni tarjetas en esta fase. Si no hay URL aprobada, el CTA debe derivar al contacto general.

## Dirección visual

### Personalidad

- natural;
- cálida;
- sobria;
- institucional sin rigidez;
- emocional sin culpa ni dramatización.

### Paleta orientativa

Usar como guía, no como obligación si ya existe branding:

- fondo crema: `#F7F4EC`;
- verde profundo: `#244137`;
- terracota cálida: `#B96E46`;
- arena: `#D7C6A8`;
- texto oscuro: `#202522`;
- blanco cálido: `#FFFDFC`.

Debe cumplir contraste AA.

### Tipografía

- titulares: serif cálida o humanista, sin aspecto ornamental excesivo;
- cuerpo y UI: sans serif muy legible;
- evitar estética infantil, western, veterinaria genérica o lujo artificial.

### Fotografía

- priorizar planos naturales y dignos;
- combinar retratos de caballos con escenas de manada;
- evitar fotos diseñadas para generar lástima;
- no mostrar heridas o sufrimiento como recurso de conversión;
- no revelar referencias claras de ubicación;
- eliminar metadatos EXIF/GPS antes de publicar;
- generar WebP/AVIF y tamaños responsive;
- usar alt text descriptivo y sobrio.

## Componentes sugeridos

- `Header`
- `Hero`
- `TrustStrip`
- `WhatWeDo`
- `SponsorshipFeature`
- `HowSponsorshipWorks`
- `HorseGrid`
- `HorseCard`
- `HorseDetail`
- `WaysToHelp`
- `CurrentNeed`
- `Transparency`
- `AboutFoundation`
- `Partners`
- `FAQ`
- `ContactCTA`
- `Footer`

Centralizar copy, enlaces y datos en archivos de contenido/configuración. No dispersar datos institucionales en múltiples componentes.

## Requisitos técnicos

- Si existe proyecto, respetar su stack y arquitectura.
- Si se crea uno nuevo, usar un stack mantenible compatible con el entorno local de Juan; preferencia: Next.js + TypeScript + solución de estilos ya estándar en web-builder.
- Responsive desde mobile.
- HTML semántico y jerarquía de headings correcta.
- Navegación por teclado.
- Estados focus visibles.
- Imágenes optimizadas.
- Sin errores de consola.
- Sin secretos ni datos personales hardcodeados.
- Configuración de contenido separada del layout.
- No depender de servicios pagos para el preview.
- Preparar metadata, Open Graph y favicon con placeholders explícitos hasta recibir branding.
- Schema `Organization`/`NGO` solo con datos confirmados; no inventar dirección, CUIT, personería, teléfono o redes.

## Analytics preparado, no obligatorio

Si el proyecto ya tiene analytics, instrumentar sin PII:

- `horse_card_opened`;
- `horse_sponsorship_cta_clicked`;
- `help_option_clicked`;
- `whatsapp_contact_clicked`;
- `donation_interest_clicked`.

Si no existe analytics, dejar puntos de extensión o `data-*` consistentes; no agregar proveedor ni gasto en esta fase.

## Datos y activos bloqueantes para publicación

La preview puede avanzar sin estos datos. La publicación oficial no.

| Dato o activo | Responsable de validar |
|---|---|
| Logo y branding oficial | Anne / Juan |
| Dominio y repo definitivo | Juan / brain-local |
| Número de WhatsApp institucional | Anne / Juan |
| Email institucional | Anne / Juan |
| Fotos autorizadas de 6 a 10 caballos | Anne / Magalí |
| Nombre real de cada caballo | Anne / Magalí |
| Descripción pública de cada caballo | Anne / Magalí |
| Modelo de padrinazgo: compartido o exclusivo | Anne / Magalí |
| Monto y periodicidad | Anne / Magalí / Juan |
| Medio de pago o enlace aprobado | Anne / Juan |
| Periodicidad real de actualizaciones | Anne / Magalí |
| Cifra pública de caballos | Anne / Magalí |
| Datos legales publicables | Anne |
| Logos y autorización de sponsors | Anne |
| Necesidad actual y montos | Magalí / Anne |
| Política de visitas | Anne / Magalí |
| Política de privacidad / tratamiento de contactos | Anne / Juan |

## Pasos de implementación

1. Inspeccionar si existe repo local.
2. Documentar ruta y stack elegido.
3. Crear estructura base y sistema visual.
4. Implementar home completa con contenido centralizado.
5. Implementar `/apadrinar` y modelo data-driven.
6. Crear seis registros draft y placeholders locales.
7. Implementar detalle accesible y CTA configurable.
8. Agregar estados seguros para datos faltantes.
9. Revisar responsive en mobile, tablet y desktop.
10. Ejecutar lint, typecheck, tests disponibles y build de producción.
11. Levantar preview HTTP.
12. Revisar visualmente la home y `/apadrinar`; guardar capturas desktop y mobile.
13. Crear `response.md` en este handoff con evidencia.

## Criterios de aceptación

### Funcionales

- `/` y `/apadrinar` cargan sin errores.
- Navegación desktop y mobile funciona.
- Las seis fichas draft prueban el layout sin presentarse como datos reales.
- Las tarjetas se generan desde una única fuente de datos.
- Abrir/cerrar detalle de caballo funciona con mouse y teclado.
- El CTA de padrinazgo conserva el caballo seleccionado.
- No hay botones muertos: funcionan o muestran un estado pendiente explícito de preview.
- No existe integración de pagos ficticia.

### Contenido y seguridad

- No se publican nombres, historias, montos, datos legales, contacto o ubicación inventados.
- La aclaración de padrinazgo simbólico es visible.
- No se expone la ubicación del campo.
- No hay EXIF/GPS en imágenes preparadas para publicar.
- No se usan logos o fotografías externas sin autorización.
- No se promete actualización individual ni frecuencia no confirmada.

### Calidad

- Mobile, tablet y desktop verificados.
- Sin overflow horizontal.
- Contraste AA y focus visible.
- Sin errores de consola.
- Build de producción aprobado.
- Lint y typecheck aprobados o bloqueos documentados.
- Preview HTTP accesible durante la revisión.
- Capturas desktop y mobile incluidas en la respuesta.

### Estado de publicación

- Entrega inicial marcada como `PREVIEW LISTA`, no como `PUBLICADO`.
- Publicación solo después de que Juan confirme que los datos bloqueantes fueron validados por Anne/Magalí.

## Restricciones

- No publicar ni desplegar en dominio oficial sin aprobación explícita.
- No comprar dominio, hosting, plugins, imágenes o servicios.
- No crear cuentas ni aprobar gastos.
- No inventar datos institucionales o historias de caballos.
- No usar culpa, morbo o imágenes de sufrimiento como recurso comercial.
- No publicar ubicación exacta, mapa ni referencias sensibles del campo.
- No hardcodear credenciales, tokens, datos bancarios ni PII.
- No modificar `Hermes/Config/`.
- No escribir código en el vault compartido.
- No hacer cambios destructivos.

## Respuesta esperada

Crear:

```text
Hermes/Handoffs/vps-to-local/HO-2026-08-03-001/response.md
```

Formato mínimo:

```text
Estado: PREVIEW LISTA / PARCIAL / BLOQUEADO

Proyecto:
- Ruta absoluta:
- Stack:
- Reutilizado o creado:

Rutas implementadas:
- /:
- /apadrinar:

Preview:
- URL HTTP:
- Captura desktop:
- Captura mobile:

Funcionalidad:
- Navegación mobile:
- Grilla data-driven:
- Detalle de caballo:
- CTA configurable:
- Estados para datos pendientes:

Verificación:
- lint:
- typecheck:
- tests:
- build:
- errores de consola:

Archivos principales modificados:
-

Datos todavía bloqueantes:
-

Decisión:
- Lista para revisión institucional: sí / no
- Lista para publicar: no, salvo aprobación posterior de Juan
```
