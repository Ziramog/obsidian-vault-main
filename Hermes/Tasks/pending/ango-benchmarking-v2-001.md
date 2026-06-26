═══ TAREA: Benchmarking competitivo ANGO — Argentina (V2 con scraping estructurado) ═══

Para: ANGO Metalúrgica (Antonio Gomariz)
Prioridad: Alta
Modelo: deepseek-v4-pro

═══ ANTES DE EMPEZAR ═══

Cargar la skill: b2b-competitive-scrape
Seguir su PROTOCOLO DE BÚSQUEDA ESTRUCTURADA paso por paso.

═══ CONTEXTO ═══

ANGO fabrica tomas de fuerza (PTO) con embrague industrial bajo marca RG.
60+ años en Río Tercero, Córdoba. Carcazas SAE N°6 a N°00, 1-3 discos.

El informe anterior (v1) se salteó al mayor productor de embruges de Argentina.
Eso NO puede pasar otra vez. El problema fue responder con conocimiento del
modelo en lugar de buscar sistemáticamente.

═══ QUÉ BUSCAR (con web_search OBLIGATORIO) ═══

Producto para las búsquedas:
- Español: "toma de fuerza", "toma de fuerza con embrague", "PTO industrial", "embrague industrial", "embrague PTO"
- Inglés: "PTO clutch", "power take off clutch", "industrial clutch"

Ejecutar MÍNIMO 20 búsquedas web siguiendo la skill b2b-competitive-scrape:

Fase 1 — Términos españoles (mínimo 8 búsquedas):
- "toma de fuerza fabricante Argentina"
- "toma de fuerza con embrague fabrica Argentina"
- "embrague industrial fabricante Argentina"
- "PTO industrial Argentina empresa"
- "fabricantes de tomas de fuerza en Argentina"
- "toma de fuerza marca Argentina"
- "embrague industrial Córdoba"
- "toma de fuerza Buenos Aires"

Fase 2 — Términos ingleses (mínimo 5 búsquedas):
- "PTO clutch manufacturer Argentina"
- "industrial clutch supplier Argentina"
- "power take off clutch South America"
- "PTO clutch Brazil Argentina"
- "industrial clutch Argentina market"

Fase 3 — Taxonomía industrial (mínimo 5 búsquedas):
- "guía industrial toma de fuerza Argentina"
- "directorio PTO clutch Argentina site:kompass.com"
- "fabricantes embragues Argentina AFARTEC"
- "cámara fabricantes maquinaria agrícola Argentina PTO"
- "fabricantes embragues industriales Argentina directorio"

Fase 4 — Marcas importadas conocidas (mínimo 5 búsquedas):
- "distribuidor Walterscheid Argentina"
- "distribuidor Bondioli Pavesi Argentina"
- "distribuidor WPT Power Argentina"
- "distribuidor Twin Disc Argentina"
- "distribuidor Comer Argentina"

Fase 5 — Para cada empresa encontrada:
- web_extract su sitio web
- Buscar "{empresa} productos" y "{empresa} clientes"
- Verificar si fabrica PTO con embrague o solo distribuye

Fase 6 — Datos de mercado:
- "importación toma de fuerza Argentina NCM"
- "mercado PTO Argentina estadística"

═══ ENTREGABLE ═══

Escribir en: companies/ango/research/benchmarking-competencia-ango-argentina-2026-06-25-v2.md

Para cada empresa: nombre, URL de fuente (OBLIGATORIO), productos, marca, ubicación, web, contacto, relevancia (1-5⭐), si fabrica o distribuye.

MÍNIMO de empresas a identificar: 15 (entre fabricantes, importadores y distribuidores).

Al cerrar: actualizar companies/ango/intelligence/patterns.md.