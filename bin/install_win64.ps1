# FFmpeg installation script for Windows 64-bit
# Downloads and installs FFmpeg to bin/win/x64

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = Join-Path $ScriptDir "win\x64"
$TempDir = Join-Path $env:TEMP "ffmpeg-install-$(Get-Random)"

Write-Host "Installing FFmpeg to $TargetDir..."

# Create target directory if it doesn't exist
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

# Create temp directory
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

try {
    # Download FFmpeg
    Write-Host "Downloading FFmpeg..."
    $ZipPath = Join-Path $TempDir "ffmpeg.zip"
    curl.exe -L -o $ZipPath "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    Write-Host "Download completed: $ZipPath"

    # Extract
    Write-Host "Extracting FFmpeg..."
    Expand-Archive -Path $ZipPath -DestinationPath $TempDir

    # Find and copy ffmpeg.exe
    Write-Host "Installing ffmpeg.exe..."
    $ffmpegExe = Get-ChildItem -Path $TempDir -Recurse -Filter "ffmpeg.exe" -ErrorAction SilentlyContinue | Select-Object -First 1

    if (-not $ffmpegExe) {
        throw "ffmpeg.exe not found in the downloaded package"
    }

    Copy-Item -Path $ffmpegExe.FullName -Destination (Join-Path $TargetDir "ffmpeg.exe") -Force

    Write-Host "FFmpeg installed successfully at $TargetDir\ffmpeg.exe"
}
finally {
    # Cleanup
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force
    }
}
