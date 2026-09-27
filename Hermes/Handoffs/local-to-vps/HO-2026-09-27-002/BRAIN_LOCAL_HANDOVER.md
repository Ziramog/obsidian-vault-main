# 🧠 Hermes PWA — Documento de Traspaso & Plan de Despliegue en VPS
> **Destinatario:** `brain-local` (Orquestador & Coordinador Principal — Wolfim Studio)  
> **Fecha:** 27 de Septiembre, 2026  
> **Proyecto:** `hermes-pwa` (Cliente Mobile PWA para Hermes Agent Gateway)  
> **Ubicación actual en PC:** `C:\Projects\hermes-pwa`  
> **VPS Destino:** `vmi3131751` (`100.124.132.48`) en Tailscale  

---

## 1. Resumen Ejecutivo & Misión de Brain Local

La aplicación **Hermes PWA** ha sido completamente rediseñada bajo estándares **Apple Human Interface / Off-White UI**, optimizada para acceso móvil desde la calle vía **4G/5G** a través de **Tailscale**.

### Tu Misión:
Desplegar y mantener corriendo **Hermes PWA** en el **VPS Linux (`vmi3131751`)** de forma persistente (24/7), desacoplándola de la PC local Windows (`truzt`). De esta manera, el usuario podrá acceder siempre a sus bots desde cualquier dispositivo móvil sin requerir que la PC de escritorio esté encendida.

---

## 2. Arquitectura del Proyecto

### Stack Tecnológico:
- **Framework:** Next.js 16.3.6 (App Router, Webpack).
- **Lenguaje:** TypeScript + React 19.
- **Estilos:** Tailwind CSS con tokens semánticos Apple Off-White (`#f5f5f7` canvas, bordes sutiles, modo claro/oscuro persistente).
- **Componentes & Animaciones:** Lucide React + Framer Motion (transiciones tipo app nativa iOS).
- **PWA & Offline:** `@ducanh2912/next-pwa` con Service Worker (`public/sw.js`) y `public/manifest.json`.
- **Estado Global:** Zustand (`src/lib/store.ts`).

### Conexión con Hermes (Arquitectura Híbrida Multi-Nodo):
La PWA ahora opera en modo **Multi-Nodo**, permitiendo unificar en una sola pantalla tanto los bots de la **PC local** como los del **VPS**:
- **Variable `HERMES_API_URL`:** URL base del gateway local del host donde corre la PWA (por defecto `http://127.0.0.1:8642`).
- **Variable `HERMES_VPS_URL`:** URL del gateway secundario (en la PC apunta al VPS `http://100.124.132.48:8642`; cuando corra en el VPS puede apuntar de vuelta a la PC `http://100.105.0.23:8642`).
- **Variable `HERMES_VPS_API_KEY`:** (Opcional) Clave de autenticación para el gateway secundario si difiere de la principal.
- **Variable `HERMES_HOME`:** Directorio raíz de datos de Hermes (`~/.hermes` en Linux o `%LOCALAPPDATA%\hermes` en Windows).
- **Directorio de Perfiles (`HERMES_HOME/profiles`):** Contiene la configuración individual de cada bot (`config.yaml`), historial de sesiones (`sessions/*.json`), memorias y herramientas.

---

## 3. Características Clave & Funcionalidades Implementadas

1. **Directorio de Bots Unificado (PC Local + VPS):**
   - [`src/components/BotDirectory.tsx`](src/components/BotDirectory.tsx): Vista principal con buscador de bots por nombre o rol.
   - **Badges de Origen del Bot:**
     - 🖥️ **PC Local** (bots alojados en la máquina Windows).
     - ☁️ **VPS** (bots descubiertos y ejecutados en el servidor Linux).
2. **Detección de Presencia Online / Offline:**
   - La API (`GET /api/profiles`) sondea cada perfil con un timeout de 2 segundos.
   - Bots con runner activo muestran 🟢 **Online** con halo verde; bots inaccesibles o dependientes de la PC local apagada muestran ⚪ **Offline**.
   - En [`src/components/ChatView.tsx`](src/components/ChatView.tsx), si un bot está offline, se despliega una barra de advertencia amarilla indicando que requiere la PC local.
3. **Enrutamiento Inteligente Multi-Nodo (`/api/chat` y `/api/sessions`):**
   - Cuando el usuario chatea con un bot de la PC, la PWA canaliza la petición a `HERMES_API_URL`.
   - Cuando chatea con un bot del VPS, la PWA redirige de forma transparente la petición al gateway del VPS (`HERMES_VPS_URL`), enviando y recibiendo streaming sin fricción.
4. **Selector Dinámico de Modelos de AI por Bot:**
   - En la cabecera de cada chat hay una píldora interactiva con el modelo actual (ej: `deepseek-v4.1-flash ▾`).
   - Al tocarla, abre un *BottomSheet* que permite cambiar el modelo en caliente a:
     - `deepseek-v4.1-flash`
     - `gemini-3.8-flash`
     - `gemini-3.7-flash`
     - `gemini-3.5-flash-lite`
     - `claude-3-7-sonnet`
     - `gpt-4o`
     - `qwen3.8-flash`
     - O ingresar cualquier string personalizado de OpenRouter u otro proveedor.
   - El endpoint `PATCH /api/profiles` actualiza el `config.yaml` del perfil directamente en disco sin necesidad de reiniciar la app.
5. **Comportamiento Mobile Nativo (Estilo X/Twitter & iMessage):**
   - **En el Hub (Inicio):** El header superior y el `BottomNav` se ocultan suavemente al hacer scroll hacia abajo y reaparecen al deslizar hacia arriba.
   - **Dentro del Chat:** El `BottomNav` se retira automáticamente (`hidden={hideNavs || isChatOpen}`) y el chat sube a `z-[70]`. La caja de texto (composer) se adhiere limpiamente al fondo (`pb-safe`) garantizando visibilidad completa y compatibilidad nativa con el teclado virtual de Android/iOS.
6. **Salas Grupales (Group Chat):**
   - Sincronización en tiempo real y soporte para menciones `@bot` en salas multi-agente (`src/components/GroupChatView.tsx`).

---

## 4. Endpoints Internos de la PWA (`src/app/api/`)

| Ruta | Método | Descripción |
|---|---|---|
| `/api/auth/validate` | `POST` | Valida la API Key contra `${HERMES_API_URL}/v1/models`. |
| `/api/profiles` | `GET` | Lista todos los perfiles de bots, sus modelos, sesiones y estado Online/Offline. |
| `/api/profiles` | `PATCH` | Recibe `{ profile, model }` y actualiza el archivo `config.yaml` del bot en disco. |
| `/api/chat` | `POST` | Reenvía el streaming SSE a `${HERMES_API_URL}/p/${profile}/v1/chat/completions`. |
| `/api/sessions` | `GET`, `POST` | Lista o crea sesiones de chat para un perfil específico. |
| `/api/sessions/[sessionId]` | `DELETE` | Elimina una conversación del historial. |
| `/api/sessions/[sessionId]/messages` | `GET` | Recupera el historial de mensajes de una conversación. |
| `/api/groups` | `GET` | Lista las salas multi-agente configuradas. |
| `/api/groups/[groupId]/chat` | `POST` | Streaming colaborativo en salas grupales. |
| `/api/groups/[groupId]/messages` | `GET` | Historial de mensajes de una sala grupal. |

---

## 5. Guía de Despliegue en el VPS (`vmi3131751`)

Sigue estos pasos ordenados para montar la aplicación en el servidor:

### Paso 1: Acceso al VPS y Verificación del Entorno
Conéctate por SSH al VPS mediante la red de Tailscale:
```bash
ssh root@100.124.132.48
# O utilizando Tailscale SSH si está habilitado:
# tailscale ssh root@vmi3131751
```

Verifica que Node.js esté instalado (versión 20 o superior recomendada):
```bash
node -v   # Debe ser >= v20.x
npm -v
git --version
```
*Si Node.js no está instalado o es una versión vieja, instálalo con NodeSource:*
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
```

### Paso 2: Clonar o Transferir el Código
Ubica el proyecto en una ruta estándar del servidor, por ejemplo `/opt/hermes-pwa`:
```bash
git clone <URL_DEL_REPOSITORIO> /opt/hermes-pwa
# O si transfieres los archivos desde la PC:
# rsync -avz --exclude 'node_modules' --exclude '.next' c:/Projects/hermes-pwa/ root@100.124.132.48:/opt/hermes-pwa/
cd /opt/hermes-pwa
```

### Paso 3: Configurar Variables de Entorno Multi-Nodo (`.env.local`)
Crea el archivo `.env.local` en `/opt/hermes-pwa/.env.local`:
```bash
cat << 'EOF' > /opt/hermes-pwa/.env.local
# Gateway principal local en el VPS (para todos los bots 24/7 de Linux)
HERMES_API_URL=http://127.0.0.1:8642

# Ruta al directorio .hermes en el VPS donde residen los profiles y configs
HERMES_HOME=/root/.hermes

# Gateway secundario hacia la PC local (para descubrir los bots de Windows cuando la PC esté prendida)
HERMES_VPS_URL=http://100.105.0.23:8642
EOF
```
*(Nota: Ajusta `HERMES_HOME` a la ruta real de tu instalación de Hermes en el VPS. La IP `100.105.0.23` corresponde a la máquina Windows `truzt` en Tailscale).*

### Paso 4: Instalar Dependencias y Compilar
```bash
npm install
npm run build
```
*(Asegúrate de que la compilación concluya con código 0 y genere la ruta estática y las 10 rutas dinámicas).*

### Paso 5: Configurar Daemon Persistente con PM2
Para que el servidor se mantenga activo ante reinicios o desconexiones:
```bash
npm install -g pm2
pm2 start npm --name "hermes-pwa" -- run start
pm2 save
pm2 startup
```
Verifica que el servicio esté corriendo:
```bash
pm2 status
curl -I http://127.0.0.1:3000
# Debe devolver HTTP/1.1 200 OK
```

### Paso 6: Exponer con HTTPS mediante Tailscale Serve
Para que la PWA sea accesible desde el celular con HTTPS y PWA habilitada:
```bash
tailscale serve --bg 3000
```
Verifica el estado del túnel:
```bash
tailscale serve status
# Deberá mostrar:
# https://vmi3131751.<tu-tailnet>.ts.net (tailnet only)
# |-- / proxy http://127.0.0.1:3000
```

---

## 6. Verificación Posterior al Despliegue

Una vez levantado en el VPS:
1. Desde el navegador móvil en 4G o Wi-Fi, ingresa a:
   `https://vmi3131751.<tu-tailnet>.ts.net`
2. Ingresa tu API Key de Hermes (la configurada en el gateway del VPS).
3. Comprueba que el **Directorio de Bots** cargue correctamente:
   - Los bots propios del VPS aparecerán con 🟢 **Online**.
   - Los bots que residan exclusivamente en la PC de escritorio aparecerán con ⚪ **Offline** cuando la PC esté apagada.
4. Abre un chat, comprueba que la caja de texto se encuentre despejada y prueba cambiar el modelo desde la cabecera tocando la píldora de modelo.

---

## 7. Convenciones de Equipo (Wolfim Studio)
- **No commit / push sin autorización explícita.**
- **No revelar secretos ni tokens en logs o commits.**
- Mantener este documento actualizado ante futuros cambios de arquitectura.
