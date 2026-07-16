# ANGO — Paso a paso para llevar adelante la campaña de Google Ads

**Fecha:** 2026-07-07  
**Tipo:** Instructivo interno operativo  
**No es propuesta comercial**  
**Objetivo:** configurar, lanzar y optimizar una campaña real de Google Ads para ANGO.

---

## 0. Idea central

La campaña no se plantea como una venta formal a ANGO. Se plantea como un trabajo operativo para probar si Google Ads puede generar consultas reales para ANGO.

El enfoque correcto es:

```text
Empezar chico → medir → aprender → ajustar → escalar solo si funciona
```

Presupuesto inicial recomendado para pauta:

```text
USD 100 por mes en Google Ads
```

Con ese monto no buscamos volumen masivo. Buscamos validar si hay demanda real y qué términos usan los compradores.

---

## 1. Qué vamos a promocionar

La campaña tiene dos focos:

### Foco A — Repuestos Urvig

Este es el foco principal para arrancar.

Motivo:

- Urvig tiene equipos instalados.
- Hay usuarios que necesitan repuestos.
- Según lo conversado, hay dolor por precio, demora o postventa.
- Si alguien busca “repuestos Urvig”, ya tiene una necesidad concreta.

### Foco B — Tomas de fuerza industriales ANGO

Este es el segundo foco.

Importante: no son tomas de fuerza para camiones, tractores, mixers, bateas ni grúas.

Son tomas de fuerza con embrague para motores industriales estacionarios.

Aplicaciones:

- motobombas,
- motores diésel grandes,
- bombas de riego,
- bombas de pozo,
- compresores,
- generadores,
- equipos industriales,
- petróleo,
- minería.

---

## 2. Estructura recomendada

Con USD 100/mes no conviene dividir en muchas campañas.

Crear una sola campaña:

```text
Campaña: ANGO - Search - Industrial - 2026
```

Dentro de esa campaña crear dos grupos de anuncios:

```text
Grupo 1: Repuestos Urvig
Grupo 2: Tomas de Fuerza Industriales
```

Por qué así:

- concentra presupuesto,
- facilita revisar datos,
- evita que Google disperse el gasto,
- permite comparar qué foco funciona mejor.

---

## 3. Antes de entrar a Google Ads

Confirmar estos datos:

- [ ] URL exacta del sitio de ANGO.
- [ ] Página destino para repuestos Urvig.
- [x] Página destino para tomas de fuerza industriales.
- [ ] WhatsApp o teléfono correcto para consultas.
- [ ] Email correcto para consultas: `juan@wolfim.com` si se usa Juan como contacto.
- [ ] Modelos Urvig para los que ANGO tiene repuestos.
- [ ] Zonas donde ANGO puede vender o enviar sin problema.
- [ ] Quién va a responder las consultas.

Si no hay página específica para Urvig, se puede arrancar con la página más cercana, pero lo ideal es crear una landing simple.

---

## 4. Crear o preparar la cuenta de Google Ads

### Paso 4.1 — Entrar a Google Ads

Ir a:

```text
https://ads.google.com/
```

Entrar con la cuenta de Google que se vaya a usar para ANGO.

### Paso 4.2 — Configuración básica

Verificar:

- país: Argentina,
- moneda: la que corresponda según cuenta/facturación,
- zona horaria: Argentina,
- método de pago cargado,
- acceso para Juan si corresponde.

### Paso 4.3 — No crear campaña inteligente

Google suele empujar “campañas inteligentes” o modos automáticos.

Evitar al inicio:

- campaña inteligente,
- Performance Max,
- Display,
- YouTube,
- Demand Gen.

Elegir campaña manual de búsqueda.

---

## 5. Medición mínima antes de publicar

No conviene gastar aunque sea poco si no podemos saber qué funcionó.

Mínimo necesario:

- [ ] Google Analytics 4 instalado.
- [ ] Google Ads vinculado con GA4.
- [ ] Auto-tagging activado en Google Ads.
- [ ] Conversiones básicas creadas.

### Conversiones recomendadas

| Conversión | Qué mide | Prioridad |
|---|---|---|
| `whatsapp_clicked` | clic en botón WhatsApp | Alta |
| `lead_form_submitted` | envío de formulario | Alta |
| `email_clicked` | clic en email | Media |
| `phone_clicked` | clic en teléfono | Media |

### Si no podemos instalar tracking todavía

Se puede lanzar igual como prueba muy básica, pero anotando manualmente:

- fecha de consulta,
- qué preguntó,
- si dijo que vino de Google,
- producto consultado,
- si cotizó o no.

Pero lo ideal es medir desde el día 1.

---

## 6. Crear la campaña en Google Ads

En Google Ads:

```text
Campañas → Nueva campaña
```

### Configuración

**Objetivo:** Leads o campaña sin objetivo guiado  
**Tipo:** Búsqueda  
**Nombre:** `ANGO - Search - Industrial - 2026`  
**Redes:** solo Red de Búsqueda  
**Desactivar:** Red de Display  
**Ubicación:** Argentina  
**Idioma:** Español  
**Presupuesto:** equivalente a USD 100/mes  

### Presupuesto diario

Si el presupuesto mensual es USD 100:

```text
USD 100 / 30 días = USD 3,33 por día aprox.
```

Cargar el equivalente diario en la moneda de la cuenta.

### Puja inicial

Recomendación inicial:

- empezar con maximizar clics con límite de CPC si Google lo permite,
- o CPC manual si está disponible,
- evitar maximizar conversiones hasta tener datos.

Motivo: al inicio no hay conversiones suficientes para que Google optimice bien.

---

## 7. Grupo de anuncios 1 — Repuestos Urvig

Crear grupo:

```text
Repuestos Urvig
```

### Keywords

Usar coincidencia exacta y de frase. No usar amplia al inicio.

```text
"repuestos Urvig"
[repuestos Urvig]
"repuesto Urvig"
"repuesto embrague Urvig"
"repuestos embrague Urvig"
"repuestos toma de fuerza Urvig"
"Urvig repuestos Argentina"
"Urvig service"
"Urvig postventa"
"alternativa repuestos Urvig"
"repuestos compatibles Urvig"
```

### Anuncio sugerido

#### Títulos

```text
Repuestos Urvig
Repuestos para Embragues Urvig
Alternativa a Repuestos Urvig
Fabricación Nacional
Consultá por tu Modelo
ANGO Metalúrgica
```

#### Descripciones

```text
Repuestos compatibles para embragues Urvig. Fabricación nacional. Consultá por modelo y disponibilidad.

¿Problemas con repuestos Urvig? ANGO fabrica alternativas compatibles. Asesoramiento técnico directo.
```

### URL destino

Ideal:

```text
/pagina-repuestos-urvig
```

Si no existe:

- usar la página más relacionada,
- agregar botón claro de WhatsApp,
- o crear una landing simple antes de publicar.

---

## 8. Grupo de anuncios 2 — Tomas de Fuerza Industriales

Crear grupo:

```text
Tomas de Fuerza Industriales
```

### Keywords

```text
"toma de fuerza para motor industrial"
[toma de fuerza para motor industrial]
"toma de fuerza con embrague"
"toma de fuerza motor diesel"
"toma de fuerza para motobomba"
"toma de fuerza para bomba de riego"
"toma de fuerza para compresor industrial"
"toma de fuerza para generador"
"toma de fuerza fabricante Argentina"
"PTO motor diesel"
"PTO clutch Argentina"
```

### Anuncio sugerido

#### Títulos

```text
Tomas de Fuerza Industriales
Toma de Fuerza con Embrague
Para Motores Diesel Grandes
Fabricante Argentino
ANGO Metalúrgica
Asesoramiento Técnico
```

#### Descripciones

```text
Tomas de fuerza con embrague para motores industriales estacionarios. Fabricación nacional y asesoramiento técnico.

Soluciones para motobombas, compresores, generadores y equipos industriales. Consultá por aplicación.
```

---

## 9. Keywords negativas

Cargar estas negativas desde el inicio.

```text
tractor
tractores
camión
camion
camiones
volcador
volcadores
mixer
batea
grúa
grua
cosechadora
cosechadoras
cortacésped
cortacesped
mower
mercadolibre
mercado libre
amazon
pdf
gratis
manual
usado
usada
segunda mano
```

Importante:

No bloquear la palabra `repuesto`, porque para Urvig sí nos interesa.

---

## 10. Assets / extensiones

Agregar assets para mejorar visibilidad.

### Sitelinks

- Repuestos Urvig
- Tomas de Fuerza Industriales
- Consultar por WhatsApp
- ANGO Metalúrgica

### Textos destacados / callouts

- Fabricación nacional
- Río Tercero, Córdoba
- Asesoramiento técnico
- Consultá por modelo
- Repuestos compatibles

### Fragmentos estructurados

Tipo: Productos

```text
Tomas de fuerza
Embragues industriales
Repuestos Urvig
Componentes para motobombas
```

---

## 11. Revisión antes de publicar

Antes de activar la campaña revisar:

- [ ] presupuesto diario correcto,
- [ ] ubicación Argentina,
- [ ] idioma Español,
- [ ] Display desactivado,
- [ ] keywords en frase/exacta,
- [ ] negativas cargadas,
- [ ] anuncios sin promesas exageradas,
- [ ] URLs funcionando,
- [ ] WhatsApp/email correctos,
- [ ] conversiones funcionando o plan manual de registro,
- [ ] aprobación de Juan/Antonio.

No publicar si falta aprobación.

---

## 12. Primeros 7 días

No tocar todo todos los días. Google necesita algo de estabilidad.

Revisar:

- si se está gastando presupuesto,
- si hay impresiones,
- si hay clics,
- si los términos de búsqueda son correctos,
- si aparecieron consultas.

Acciones permitidas en semana 1:

- agregar negativas si aparece basura,
- corregir errores claros,
- pausar keyword evidentemente mala,
- ajustar un anuncio si tiene error.

No hacer:

- cambiar toda la estructura,
- subir presupuesto sin datos,
- activar Display,
- activar Performance Max,
- agregar keywords amplias masivas.

---

## 13. Revisión semanal

Cada semana mirar:

### 1. Términos de búsqueda

Ir a:

```text
Campañas → Insights o Keywords → Términos de búsqueda
```

Buscar:

- términos útiles,
- términos basura,
- nuevas ideas de keywords,
- palabras para negativizar.

### 2. Performance por grupo

Comparar:

- Repuestos Urvig,
- Tomas de Fuerza Industriales.

Mirar:

- impresiones,
- clics,
- CTR,
- CPC,
- consultas generadas.

### 3. Consultas reales

Registrar manualmente si hace falta:

| Fecha | Canal | Consulta | Producto | Calidad | Seguimiento |
|---|---|---|---|---|---|
| | WhatsApp/Form | | Urvig/TDF | Alta/Media/Baja | |

---

## 14. Criterio para decidir después de 30 días

Al finalizar el primer mes, responder:

1. ¿Hubo búsquedas reales?
2. ¿Qué buscó la gente exactamente?
3. ¿Hubo consultas?
4. ¿Qué grupo funcionó mejor?
5. ¿Qué términos fueron basura?
6. ¿Conviene seguir?
7. ¿Conviene subir de USD 100 a USD 150/200?

### Mantener presupuesto si:

- hubo clics relevantes,
- hubo alguna consulta,
- todavía falta volumen para decidir.

### Subir presupuesto si:

- hubo consultas buenas,
- aparece intención comercial clara,
- el presupuesto se agota y hay términos buenos,
- ANGO puede responder leads rápido.

### Pausar o replantear si:

- no hay búsquedas,
- los clics son basura,
- no hay consultas,
- la landing no convierte,
- ANGO no puede responder leads.

---

## 15. Reporte interno mensual

Formato simple:

```text
Campaña Google Ads ANGO — Mes 1

Presupuesto Google: USD ___
Clics: ___
CTR: ___
CPC promedio: USD ___
Consultas recibidas: ___
Costo por consulta: USD ___

Mejor grupo:
- Repuestos Urvig / Tomas de fuerza

Términos útiles:
- ___
- ___

Términos bloqueados:
- ___
- ___

Decisión:
- mantener / ajustar / subir / pausar

Próximo paso:
- ___
```

---

## 16. Resumen operativo

```text
1. Confirmar sitio/contacto/modelos Urvig.
2. Verificar GA4 o plan manual de seguimiento.
3. Crear campaña Search.
4. Usar solo búsqueda, no Display.
5. Crear dos grupos: Urvig y Tomas de Fuerza.
6. Cargar keywords frase/exacta.
7. Cargar negativas.
8. Cargar anuncios.
9. Activar con USD 100/mes.
10. Revisar términos semanalmente.
11. Medir consultas reales.
12. Decidir después de 30 días.
```

Este es el documento que hay que usar para ejecutar la campaña. No es una propuesta para venderle el servicio a ANGO.
