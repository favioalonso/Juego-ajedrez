@echo off
title Ajedrez en Python - Launcher
color 0A

echo ============================================================
echo                🎮 AJEDREZ EN PYTHON ♔
echo ============================================================
echo.

:menu
echo Selecciona la version del juego que deseas ejecutar:
echo.
echo 1. 🎯 Version Basica
echo 2. 🚀 Version Avanzada  
echo 3. ⭐ Version Profesional (RECOMENDADA)
echo 4. 🧪 Ejecutar Tests
echo 5. ❌ Salir
echo.

set /p choice="🎯 Elige una opcion (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🎮 Iniciando Version Basica...
    python chess_game.py
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 🎮 Iniciando Version Avanzada...
    python chess_advanced.py
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 🎮 Iniciando Version Profesional...
    python chess_professional.py
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 🧪 Ejecutando Tests...
    python test_chess.py
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 👋 ¡Gracias por usar el Ajedrez en Python!
    exit /b
)

echo ❌ Opcion no valida. Por favor, elige un numero del 1 al 5.
pause
goto menu
