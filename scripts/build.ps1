$ErrorActionPreference = "Stop"

Write-Host "[#] Building IronLantern..."

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

$SpecFile = Join-Path $ProjectRoot "packaging\IronLantern.spec"
$BuildDir = Join-Path $ProjectRoot "build"
$DistDir = Join-Path $ProjectRoot "dist"

if (-not (Test-Path $SpecFile)) {
    Write-Host "[-] Spec file not found at $SpecFile"
    exit 1
}

if (Test-Path $BuildDir) {
    Write-Host "[*] Removing previous build directory..."
    Remove-Item $BuildDir -Recurse -Force
}

if (Test-Path $DistDir) {
    Write-Host "[*] Removing previous dist directory..."
    Remove-Item $DistDir -Recurse -Force
}

Write-Host "[*] Running PyInstaller using IronLantern.spec..."

python -m PyInstaller --clean --noconfirm $SpecFile

if ($LASTEXITCODE -ne 0) {
    Write-Host "[-] IronLantern build failed."
    exit $LASTEXITCODE
}

Write-Host "[+] IronLantern build completed successfully!"
Write-Host "[+] Output directory: $DistDir"