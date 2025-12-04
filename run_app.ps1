#!/usr/bin/env pwsh
# Script de lancement de l'application AI Football Performance Analyzer
# Pour Windows PowerShell

Write-Host ""
Write-Host "========================================"
Write-Host " AI Football Performance Analyzer"
Write-Host "========================================"
Write-Host ""

# Vérifier que Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python trouvé: $pythonVersion"
} catch {
    Write-Host "❌ ERROR: Python n'est pas installé ou pas dans le PATH"
    exit 1
}

# Vérifier les modèles
$regModelPath = "models/regression_model.pkl"
$clfModelPath = "models/classification_model.pkl"

if (-not (Test-Path $regModelPath) -or -not (Test-Path $clfModelPath)) {
    Write-Host ""
    Write-Host "⚠️  WARNING: Models not found!"
    Write-Host "🔧 Training models now..."
    Write-Host ""
    
    Push-Location src
    python ml_analysis.py
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Models trained successfully!"
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Error training models!"
        exit 1
    }
}

# Lancer l'application
Write-Host "🚀 Starting Streamlit application..."
Write-Host ""
Write-Host "📱 L'app s'ouvrira dans votre navigateur à: http://localhost:8501"
Write-Host ""

streamlit run src/application.py
