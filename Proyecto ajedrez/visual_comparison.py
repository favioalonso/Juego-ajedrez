#!/usr/bin/env python3
"""
🎨 Comparador Visual de Versiones de Ajedrez
Permite ver y comparar las diferentes implementaciones visuales
"""

import sys
import os
import subprocess

def print_banner():
    print("🎨" + "=" * 58 + "🎨")
    print("            COMPARADOR VISUAL DE AJEDREZ")
    print("🎨" + "=" * 58 + "🎨")
    print()

def print_visual_menu():
    print("Elige la versión visual que quieres probar:")
    print()
    
    print("1. 🎯 Versión Original")
    print("   • Símbolos Unicode básicos")
    print("   • Interfaz simple y funcional")
    print("   ➤ Archivo: chess_game.py")
    print()
    
    print("2. ✨ Versión Mejorada (Unicode+)")
    print("   • Símbolos Unicode más grandes")
    print("   • Efectos de sombra y colores mejorados")
    print("   • Mejor renderizado de fuentes")
    print("   ➤ Archivo: chess_game.py (actualizado)")
    print()
    
    print("3. 🎨 Versión Visual Enhanced")
    print("   • Piezas dibujadas con formas geométricas")
    print("   • Efectos visuales avanzados")
    print("   • Gradientes y animaciones")
    print("   ➤ Archivo: chess_visual_enhanced.py")
    print()
    
    print("4. 🖼️ Versión Sprites Artísticos")
    print("   • Piezas dibujadas como sprites detallados")
    print("   • Efectos de sombra profesionales")
    print("   • Interfaz completamente rediseñada")
    print("   ➤ Archivo: chess_artistic_sprites.py")
    print()
    
    print("5. ⭐ Versión Profesional Completa")
    print("   • Panel lateral informativo")
    print("   • Todas las características avanzadas")
    print("   ➤ Archivo: chess_professional.py")
    print()
    
    print("6. 📊 Comparación de Características")
    print("7. ❌ Salir")
    print()

def show_comparison_table():
    """Mostrar tabla comparativa de características visuales"""
    print("📊 COMPARACIÓN DE CARACTERÍSTICAS VISUALES")
    print("=" * 80)
    print()
    
    features = [
        ("Característica", "Original", "Mejorada", "Enhanced", "Sprites", "Profesional"),
        ("-" * 15, "-" * 8, "-" * 8, "-" * 8, "-" * 7, "-" * 11),
        ("Tamaño Piezas", "Pequeño", "Grande", "Grande", "Muy Grande", "Variable"),
        ("Calidad Visual", "Básica", "Buena", "Excelente", "Premium", "Completa"),
        ("Efectos Sombra", "❌", "✅", "✅", "✅", "✅"),
        ("Gradientes", "❌", "❌", "✅", "✅", "❌"),
        ("Sprites Custom", "❌", "❌", "Formas", "Artísticos", "Unicode+"),
        ("Animaciones", "❌", "❌", "Básicas", "Avanzadas", "❌"),
        ("Panel Info", "Básico", "Básico", "Básico", "Mejorado", "Completo"),
        ("Rendimiento", "Máximo", "Alto", "Medio", "Medio", "Alto"),
        ("Tamaño Código", "Pequeño", "Pequeño", "Medio", "Grande", "Grande"),
    ]
    
    for row in features:
        print(f"{row[0]:<15} | {row[1]:<8} | {row[2]:<8} | {row[3]:<8} | {row[4]:<7} | {row[5]:<11}")
    
    print()
    print("🎨 Recomendaciones:")
    print("  • Para mejor rendimiento: Versión Original o Mejorada")
    print("  • Para mejor apariencia: Versión Sprites Artísticos")
    print("  • Para uso completo: Versión Profesional")
    print("  • Para efectos modernos: Versión Enhanced")
    print()

def run_version(script_name, description):
    """Ejecutar una versión específica"""
    try:
        if not os.path.exists(script_name):
            print(f"❌ Error: No se encontró {script_name}")
            return False
        
        print(f"🎮 Iniciando {description}...")
        print(f"📁 Ejecutando: {script_name}")
        print("=" * 50)
        
        subprocess.run([sys.executable, script_name], check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Juego cerrado por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    
    while True:
        print_banner()
        print_visual_menu()
        
        try:
            choice = input("🎯 Elige una opción (1-7): ").strip()
            print()
            
            if choice == "1":
                run_version("chess_game.py", "Versión Original con Unicode Básico")
            elif choice == "2":
                print("ℹ️  Esta es la misma que la opción 1, pero con mejoras aplicadas")
                run_version("chess_game.py", "Versión Mejorada con Unicode+")
            elif choice == "3":
                run_version("chess_visual_enhanced.py", "Versión Visual Enhanced con Formas Geométricas")
            elif choice == "4":
                run_version("chess_artistic_sprites.py", "Versión con Sprites Artísticos")
            elif choice == "5":
                run_version("chess_professional.py", "Versión Profesional Completa")
            elif choice == "6":
                show_comparison_table()
                input("Presiona Enter para continuar...")
            elif choice == "7":
                print("👋 ¡Gracias por probar las versiones visuales!")
                break
            else:
                print("❌ Opción no válida. Elige un número del 1 al 7.")
                input("Presiona Enter para continuar...")
            
            print("\n" + "🎨" + "=" * 58 + "🎨" + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Adiós!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    # Verificar archivos requeridos
    required_files = [
        "chess_game.py", 
        "chess_visual_enhanced.py", 
        "chess_artistic_sprites.py", 
        "chess_professional.py"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("❌ Error: Faltan archivos visuales:")
        for file in missing_files:
            print(f"   • {file}")
        print("\nAsegúrate de tener todos los archivos en el directorio.")
        sys.exit(1)
    
    main()
