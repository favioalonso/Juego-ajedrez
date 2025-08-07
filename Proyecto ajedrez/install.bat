@echo off
title Instalacion - Ajedrez en Python
color 0B

echo ============================================================
echo         🎮 INSTALACION - AJEDREZ EN PYTHON ♔
echo ============================================================
echo.

echo 📦 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no esta instalado o no esta en el PATH
    echo    Instala Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo 🧪 Ejecutando tests...
python test_chess.py

if errorlevel 1 (
    echo ❌ Los tests fallaron
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ ¡INSTALACION COMPLETADA EXITOSAMENTE!
echo ============================================================
echo.
echo Para jugar, ejecuta:
echo   • run_chess.bat (launcher con menu)
echo   • python chess_professional.py (version recomendada)
echo   • python launcher.py (launcher de Python)
echo.
echo ¡Disfruta del juego!
echo ============================================================

pause
