# Démarre le site LED en local sur le port 3008
# Usage : .\scripts\serve.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$Port = 3008
$Bind = "127.0.0.1"
$Url = "http://${Bind}:$Port/"

# Détecte un autre projet sur le même port (ex. Convergence26)
$listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
foreach ($conn in $listeners) {
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
  if ($proc -and $proc.CommandLine -notmatch "led-initiative") {
    Write-Host "ATTENTION : le port $Port est deja utilise par un autre projet :" -ForegroundColor Red
    Write-Host $proc.CommandLine -ForegroundColor Yellow
    Write-Host "Arretez ce serveur avant de lancer LED, ou changez de port." -ForegroundColor Yellow
    exit 1
  }
}

Write-Host "Generation des PDFs..." -ForegroundColor Cyan
python scripts/generate_pdfs.py

Write-Host "Demarrage MkDocs sur $Url ..." -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arreter." -ForegroundColor DarkGray
Write-Host ""

Start-Process $Url
mkdocs serve -a "${Bind}:$Port"
