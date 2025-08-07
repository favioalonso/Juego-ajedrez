#!/usr/bin/env python3
"""
🎮 Launcher para el Juego de Ajedrez en Python
Permite elegir qué versión del juego ejecutar
"""

import sys
import os
import subprocess

def print_banner():
    print("=" * 60)
    print("🎮             AJEDREZ EN PYTHON               ♔")
    print("=" * 60)
    print()

def print_menu():
    print("Selecciona la versión del juego que deseas ejecutar:")
    print()
    print("1. 🎯 Versión Básica (chess_game.py)")
    print("   • Funcionalidad básica mejorada")
    print("   • Símbolos Unicode más grandes")
    print()
    print("2. 🚀 Versión Avanzada (chess_advanced.py)")
    print("   • Detección de jaque y jaque mate")
    print("   • Validación completa de movimientos")
    print()
    print("3. ⭐ Versión Profesional (chess_professional.py)")
    print("   • Panel lateral con información completa")
    print("   • Cronómetro y balance de material")
    print("   • Guardado de partidas")
    print()
    print("4. 🎨 Versión Visual Enhanced (chess_visual_enhanced.py)")
    print("   • Piezas con formas geométricas")
    print("   • Efectos visuales avanzados")
    print()
    print("5. 🖼️ Versión Sprites Artísticos (chess_artistic_sprites.py)")
    print("   • Piezas dibujadas como sprites detallados")
    print("   • Máxima calidad visual")
    print()
    print("6. 🎨 Comparador Visual")
    print("7. 🧪 Ejecutar Tests")
    print("8. 📖 Ver README")
    print("9. ❌ Salir")
    print()

def run_game(script_name):
    """Ejecutar un script del juego"""
    try:
        print(f"🎮 Iniciando {script_name}...")
        print("=" * 50)
        
        # Verificar que el archivo existe
        if not os.path.exists(script_name):
            print(f"❌ Error: No se encontró el archivo {script_name}")
            return False
        
        # Ejecutar el script
        subprocess.run([sys.executable, script_name], check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Juego interrumpido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def show_readme():
    """Mostrar el contenido del README"""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            print("📖 README.md")
            print("=" * 50)
            print(content)
            print("=" * 50)
    except FileNotFoundError:
        print("❌ No se encontró el archivo README.md")
    except Exception as e:
        print(f"❌ Error leyendo README: {e}")

def main():
    """Función principal del launcher"""
    
    while True:
        print_banner()
        print_menu()
          try:
            choice = input("🎯 Elige una opción (1-9): ").strip()
            print()
            
            if choice == "1":
                run_game("chess_game.py")
            elif choice == "2":
                run_game("chess_advanced.py")
            elif choice == "3":
                run_game("chess_professional.py")
            elif choice == "4":
                run_game("chess_visual_enhanced.py")
            elif choice == "5":
                run_game("chess_artistic_sprites.py")
            elif choice == "6":
                run_game("visual_comparison.py")
            elif choice == "7":
                run_game("test_chess.py")
            elif choice == "8":
                show_readme()
                input("\nPresiona Enter para continuar...")
            elif choice == "9":
                print("👋 ¡Gracias por usar el Ajedrez en Python!")
                break
            else:
                print("❌ Opción no válida. Por favor, elige un número del 1 al 9.")
                input("Presiona Enter para continuar...")
            
            print("\n" + "=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Adiós!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":    # Verificar que estamos en el directorio correcto
    required_files = [
        "chess_game.py", "chess_advanced.py", "chess_professional.py", 
        "chess_visual_enhanced.py", "chess_artistic_sprites.py",
        "test_chess.py", "visual_comparison.py"
    ]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("❌ Error: Faltan archivos del juego:")
        for file in missing_files:
            print(f"   • {file}")
        print("\nAsegúrate de estar en el directorio correcto del proyecto.")
        sys.exit(1)
    
    main()
