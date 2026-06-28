<# 
.SYNOPSIS
    Organiza archivos de C:\Users\ingju\Downloads por tipo en subcarpetas.
    Disenado para ejecucion diaria via Task Scheduler (PC Brain protocol).
.DESCRIPTION
    Clasifica archivos sueltos por extension a carpetas tematicas:
    Documentos, Imagenes, Videos, Audio, Instaladores, Comprimidos.
    Gestiona un Cesto_Diario (vaciado diario) con Papelera_Local (3 dias).
    No toca subdirectorios creados manualmente ni desktop.ini.
    Genera reporte en el vault de Obsidian.
.PARAMETER DryRun
    Si es true, solo reporta lo que haria sin ejecutar movimientos.
.PARAMETER LogPath
    Ruta completa para el archivo de reporte .md. Por defecto se genera
    en el vault de Obsidian con marca de tiempo.
.PROTOCOL
    PC Brain: lectura + movimientos controlados. No elimina sin papelera.
    No modifica archivos del sistema. No toca directorios existentes.
.NOTES
    Encoding: UTF-8 with BOM (PowerShell requirement)
    Evitar % en strings interpolados, usar concatenacion +.
    Evitar em dashes y acentos en strings de codigo.
#>

param(
    [switch]$DryRun = $false,
    [string]$LogPath = ""
)

# ============================================================
# CONFIGURACION
# ============================================================
$Downloads = "$env:USERPROFILE\Downloads"
$VaultReports = "C:\Projects\Obsidian\obsidian-vault-main\Systems\Local-PC\Reports"
$ScriptName = "Organize-Downloads"
$StartTime = Get-Date

# Carpetas de clasificacion (el prefijo _ las ordena primero en el explorer)
$Folders = @(
    "_Inbox",
    "Documentos",
    "Imagenes",
    "Videos",
    "Audio",
    "Instaladores",
    "Comprimidos",
    "Cesto_Diario",
    "Papelera_Local",
    "Sin_Clasificar"
)

# Mapeo de extensiones a carpeta destino
$ExtensionMap = @{
    # --- Documentos ---
    "pdf"  = "Documentos"
    "doc"  = "Documentos"
    "docx" = "Documentos"
    "epub" = "Documentos"
    "mobi" = "Documentos"
    "txt"  = "Documentos"
    "pptx" = "Documentos"
    "ppt"  = "Documentos"
    "xlsx" = "Documentos"
    "xls"  = "Documentos"
    "csv"  = "Documentos"
    "md"   = "Documentos"
    "rtf"  = "Documentos"
    "odt"  = "Documentos"
    "log"  = "Documentos"
    "json" = "Documentos"
    "winmd" = "Documentos"
    "xml"  = "Documentos"
    "html" = "Documentos"
    "htm"  = "Documentos"
    
    # --- Imagenes ---
    "jpg"  = "Imagenes"
    "jpeg" = "Imagenes"
    "png"  = "Imagenes"
    "gif"  = "Imagenes"
    "webp" = "Imagenes"
    "svg"  = "Imagenes"
    "bmp"  = "Imagenes"
    "ico"  = "Imagenes"
    "tiff" = "Imagenes"
    "tif"  = "Imagenes"
    "heic" = "Imagenes"
    "psd"  = "Imagenes"
    
    # --- Videos ---
    "mp4"  = "Videos"
    "mkv"  = "Videos"
    "avi"  = "Videos"
    "mov"  = "Videos"
    "flv"  = "Videos"
    "ts"   = "Videos"
    "webm" = "Videos"
    "wmv"  = "Videos"
    "m4v"  = "Videos"
    
    # --- Audio ---
    "mp3"  = "Audio"
    "wav"  = "Audio"
    "flac" = "Audio"
    "ogg"  = "Audio"
    "m4a"  = "Audio"
    "wma"  = "Audio"
    "aac"  = "Audio"
    "opus" = "Audio"
    
    # --- Instaladores ---
    "exe"  = "Instaladores"
    "msi"  = "Instaladores"
    "appx" = "Instaladores"
    "msix" = "Instaladores"
    
    # --- Comprimidos ---
    "zip"  = "Comprimidos"
    "rar"  = "Comprimidos"
    "7z"   = "Comprimidos"
    "tar"  = "Comprimidos"
    "gz"   = "Comprimidos"
    "cab"  = "Comprimidos"
    "bz2"  = "Comprimidos"
    "xz"   = "Comprimidos"
    "iso"  = "Comprimidos"
    "tgz"  = "Comprimidos"
}

# Archivos que NUNCA se tocan
$NeverTouch = @("desktop.ini", "Thumbs.db")

# ============================================================
# FUNCIONES
# ============================================================

function Write-Report {
    param([string]$Line)
    # Durante ejecucion acumulamos; al final escribimos el archivo
    $script:ReportLines += $Line
}

function Test-FileLocked {
    param([string]$FilePath)
    try {
        $stream = [System.IO.File]::Open($FilePath, 'Open', 'Read', 'None')
        $stream.Close()
        return $false
    }
    catch {
        return $true
    }
}

function Move-FileSafe {
    param(
        [string]$Source,
        [string]$DestFolder,
        [string]$Category
    )
    
    $fileName = Split-Path $Source -Leaf
    $destPath = Join-Path $DestFolder $fileName
    
    # Si el destino ya existe, agregar sufijo numerico
    if (Test-Path $destPath) {
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
        $ext = [System.IO.Path]::GetExtension($fileName)
        $counter = 1
        do {
            $newName = "${baseName}_(${counter})${ext}"
            $destPath = Join-Path $DestFolder $newName
            $counter++
        } while (Test-Path $destPath)
    }
    
    if ($DryRun) {
        Write-Report "- [DRY RUN] Moveria: ``$fileName`` -> ``$Category``"
        return $true
    }
    
    try {
        Move-Item -Path $Source -Destination $destPath -Force -ErrorAction Stop
        $sizeMB = [math]::Round((Get-Item $destPath).Length / 1MB, 1)
        Write-Report "- Movido: ``$fileName`` -> ``$Category`` (${sizeMB} MB)"
        return $true
    }
    catch {
        Write-Report "- ERROR moviendo ``$fileName``: $_"
        return $false
    }
}

# ============================================================
# INICIALIZACION
# ============================================================

$script:ReportLines = @()
$movedCount = 0
$cestoCount = 0
$papeleraCount = 0
$errorCount = 0

Write-Report "# Reporte: Organizacion de Downloads"
Write-Report ""
Write-Report "**Fecha:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Report "**Equipo:** $env:COMPUTERNAME"
Write-Report "**Usuario:** $env:USERNAME"
Write-Report "**Modo:** $(if ($DryRun) { 'DRY RUN (simulacion)' } else { 'EJECUCION REAL' })"
Write-Report ""

# ============================================================
# PASO 1: Crear estructura de carpetas
# ============================================================

Write-Report "## 1. Estructura de carpetas"
Write-Report ""

foreach ($folder in $Folders) {
    $folderPath = Join-Path $Downloads $folder
    if (-not (Test-Path $folderPath)) {
        if (-not $DryRun) {
            New-Item -Path $folderPath -ItemType Directory -Force | Out-Null
        }
        Write-Report "- Carpeta creada: ``$folder/``"
    }
    else {
        Write-Report "- Carpeta existente: ``$folder/``"
    }
}

# ============================================================
# PASO 2: Clasificar archivos sueltos de la raiz de Downloads
# ============================================================

Write-Report ""
Write-Report "## 2. Clasificacion de archivos sueltos"
Write-Report ""

$rootItems = Get-ChildItem -Path $Downloads -File -Force | Where-Object { $_.Name -notin $NeverTouch }

if ($rootItems.Count -eq 0) {
    Write-Report "No hay archivos sueltos en la raiz de Downloads."
}
else {
    Write-Report "Se encontraron $($rootItems.Count) archivo(s) en la raiz."
    Write-Report ""
    
    foreach ($item in $rootItems) {
        $ext = $item.Extension.TrimStart('.').ToLower()
        
        # Si no tiene extension
        if ([string]::IsNullOrEmpty($ext)) {
            Write-Report "- Sin extension: ``$($item.Name)`` -> ``Sin_Clasificar/``"
            if (-not $DryRun) {
                try {
                    $destPath = Join-Path (Join-Path $Downloads "Sin_Clasificar") $item.Name
                    Move-Item -Path $item.FullName -Destination $destPath -Force
                    $movedCount++
                } catch {
                    Write-Report "  ERROR: $_"
                    $errorCount++
                }
            }
            else { $movedCount++ }
            continue
        }
        
        # Buscar en el mapeo
        if ($ExtensionMap.ContainsKey($ext)) {
            $category = $ExtensionMap[$ext]
            $destFolder = Join-Path $Downloads $category
            
            # Verificar que no este bloqueado (descarga en progreso)
            if (Test-FileLocked $item.FullName) {
                Write-Report "- BLOQUEADO (en uso): ``$($item.Name)`` -> se salta hasta la proxima ejecucion"
                continue
            }
            
            if (Move-FileSafe -Source $item.FullName -DestFolder $destFolder -Category $category) {
                $movedCount++
            }
            else {
                $errorCount++
            }
        }
        else {
            # Extension no reconocida
            $sizeMB = [math]::Round($item.Length / 1MB, 1)
            Write-Report "- No clasificado: ``$($item.Name)`` (.$ext, ${sizeMB} MB) -> ``Sin_Clasificar/``"
            if (-not $DryRun) {
                try {
                    $destPath = Join-Path (Join-Path $Downloads "Sin_Clasificar") $item.Name
                    Move-Item -Path $item.FullName -Destination $destPath -Force
                    $movedCount++
                } catch {
                    Write-Report "  ERROR: $_"
                    $errorCount++
                }
            }
            else { $movedCount++ }
        }
    }
}

# ============================================================
# PASO 3: Vaciar Cesto_Diario -> Papelera_Local
# ============================================================

Write-Report ""
Write-Report "## 3. Vaciado de Cesto_Diario"
Write-Report ""

$cestoPath = Join-Path $Downloads "Cesto_Diario"
$papeleraPath = Join-Path $Downloads "Papelera_Local"

if (Test-Path $cestoPath) {
    $cestoItems = Get-ChildItem -Path $cestoPath -Force -ErrorAction SilentlyContinue
    
    if ($cestoItems.Count -eq 0) {
        Write-Report "Cesto_Diario vacio. Nada que procesar."
    }
    else {
        $today = Get-Date -Format "yyyy-MM-dd"
        $cestoDestFolder = Join-Path $papeleraPath "cesto_${today}"
        
        if (-not $DryRun) {
            if (-not (Test-Path $cestoDestFolder)) {
                New-Item -Path $cestoDestFolder -ItemType Directory -Force | Out-Null
            }
        }
        
        Write-Report "Moviendo $($cestoItems.Count) item(s) a Papelera_Local/cesto_${today}/ ..."
        
        foreach ($item in $cestoItems) {
            $destPath = Join-Path $cestoDestFolder $item.Name
            
            if ($DryRun) {
                Write-Report "- [DRY RUN] Moveria: ``$($item.Name)`` -> ``Papelera_Local/cesto_${today}/``"
                $cestoCount++
            }
            else {
                try {
                    Move-Item -Path $item.FullName -Destination $destPath -Force -ErrorAction Stop
                    Write-Report "- Movido a papelera: ``$($item.Name)``"
                    $cestoCount++
                }
                catch {
                    Write-Report "- ERROR moviendo ``$($item.Name)`` de Cesto_Diario: $_"
                    $errorCount++
                }
            }
        }
    }
}

# ============================================================
# PASO 4: Limpiar Papelera_Local (+3 dias)
# ============================================================

Write-Report ""
Write-Report "## 4. Limpieza de Papelera_Local (items con +3 dias)"
Write-Report ""

if (Test-Path $papeleraPath) {
    $cutoffDate = (Get-Date).AddDays(-3)
    $oldFolders = Get-ChildItem -Path $papeleraPath -Directory -Force -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -like "cesto_*" -and $_.LastWriteTime -lt $cutoffDate
    }
    
    if ($oldFolders.Count -eq 0) {
        Write-Report "No hay items con mas de 3 dias en Papelera_Local."
    }
    else {
        Write-Report "Eliminando $($oldFolders.Count) carpeta(s) con mas de 3 dias..."
        
        foreach ($folder in $oldFolders) {
            if ($DryRun) {
                Write-Report "- [DRY RUN] Eliminaria: ``$($folder.Name)`` ($(Get-ChildItem -Path $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count) archivos)"
                $papeleraCount++
            }
            else {
                try {
                    $itemCount = (Get-ChildItem -Path $folder.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object).Count
                    Remove-Item -Path $folder.FullName -Recurse -Force -ErrorAction Stop
                    Write-Report "- Eliminado: ``$($folder.Name)`` (${itemCount} archivos)"
                    $papeleraCount++
                }
                catch {
                    Write-Report "- ERROR eliminando ``$($folder.Name)``: $_"
                    $errorCount++
                }
            }
        }
    }
}

# ============================================================
# PASO 5: Resumen y estadisticas
# ============================================================

$elapsed = [math]::Round(((Get-Date) - $StartTime).TotalSeconds, 1)

Write-Report ""
Write-Report "## 5. Resumen"
Write-Report ""
Write-Report "| Metrica | Valor |"
Write-Report "|---------|-------|"
Write-Report "| Archivos clasificados | $movedCount |"
Write-Report "| Items movidos de Cesto_Diario | $cestoCount |"
Write-Report "| Carpetas eliminadas de Papelera | $papeleraCount |"
Write-Report "| Errores | $errorCount |"
Write-Report "| Tiempo de ejecucion | ${elapsed}s |"
Write-Report ""

# Calcular espacio libre y tamaños de carpetas
$freeGB = [math]::Round((Get-PSDrive -Name (Split-Path $Downloads -Qualifier).TrimEnd(':')).Free / 1GB, 1)
Write-Report "- Espacio libre en descargas: ${freeGB} GB"
Write-Report ""

# Carpetas que mas ocupan (top 5)
Write-Report "### Carpetas mas pesadas en Downloads"
Write-Report ""
$folderSizes = @()
foreach ($folder in $Folders) {
    $folderPath = Join-Path $Downloads $folder
    if (Test-Path $folderPath) {
        $size = [math]::Round(((Get-ChildItem -Path $folderPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB), 1)
        $folderSizes += [PSCustomObject]@{ Name = $folder; SizeMB = $size }
    }
}
$folderSizes = $folderSizes | Sort-Object -Property SizeMB -Descending | Select-Object -First 5
foreach ($fs in $folderSizes) {
    Write-Report "- ``$($fs.Name)/`` = $($fs.SizeMB) MB"
}

Write-Report ""
Write-Report "---"
Write-Report "*Reporte generado por PC Brain -- Organize-Downloads.ps1*"

# ============================================================
# ESCRIBIR REPORTE A DISCO
# ============================================================

# Determinar ruta de log
if ([string]::IsNullOrEmpty($LogPath)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
    $LogPath = Join-Path $VaultReports "downloads-${timestamp}.md"
}

# Crear directorio de reports si no existe
$logDir = Split-Path $LogPath -Parent
if (-not (Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory -Force | Out-Null
}

# Escribir reporte
$ReportLines -join "`n" | Out-File -FilePath $LogPath -Encoding UTF8

Write-Output "Reporte guardado en: $LogPath"
Write-Output "Archivos clasificados: $movedCount | Cesto: $cestoCount | Papelera: $papeleraCount | Errores: $errorCount | Duracion: ${elapsed}s"
