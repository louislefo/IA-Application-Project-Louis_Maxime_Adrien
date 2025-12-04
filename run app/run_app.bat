@echo off
REM Script de lancement de l'application AI Football Performance Analyzer
REM Pour Windows

echo.
echo ========================================
echo  AI Football Performance Analyzer
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Vérifier les modèles
if not exist "models\regression_model.pkl" (
    echo.
    echo WARNING: Models not found!
    echo Training models now...
    echo.
    cd src
    python ml_analysis.py
    cd ..
    echo.
    echo Models trained successfully!
    echo.
)

REM Lancer l'application
echo Starting Streamlit application...
echo.
echo The app will open in your browser at: http://localhost:8501
echo.

streamlit run src/application.py

pause
