#!/usr/bin/env python3
"""
Script de configuración para TradeJournal API
Guía paso a paso para configurar Firebase
"""

import os
import sys

def check_requirements():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    try:
        import fastapi
        import firebase_admin
        print("✅ Dependencias instaladas correctamente")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def create_config():
    """Crear archivo de configuración desde ejemplo"""
    if not os.path.exists('config.py'):
        print("📝 Creando config.py desde config.example.py...")
        if os.path.exists('config.example.py'):
            with open('config.example.py', 'r', encoding='utf-8') as src:
                with open('config.py', 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print("✅ config.py creado. Edítalo con tus credenciales de Firebase.")
        else:
            print("❌ No se encontró config.example.py")
            return False
    else:
        print("✅ config.py ya existe")
    return True

def check_firebase_credentials():
    """Verificar configuración de Firebase"""
    print("🔥 Verificando configuración de Firebase...")

    # Buscar archivo de credenciales
    cred_paths = [
        os.path.join(os.getcwd(), 'firebase-credentials.json'),
        os.path.join(os.path.dirname(os.getcwd()), 'firebase-credentials.json'),
        '/etc/firebase-credentials.json'
    ]

    cred_file = None
    for path in cred_paths:
        if os.path.exists(path):
            cred_file = path
            break

    if cred_file:
        print(f"✅ Archivo de credenciales encontrado: {cred_file}")
        return True

    # Verificar variables de entorno
    required_env_vars = [
        'FIREBASE_PROJECT_ID',
        'FIREBASE_PRIVATE_KEY_ID',
        'FIREBASE_PRIVATE_KEY',
        'FIREBASE_CLIENT_EMAIL'
    ]

    env_vars_present = all(os.getenv(var) for var in required_env_vars)

    if env_vars_present:
        print("✅ Variables de entorno de Firebase configuradas")
        return True

    print("⚠️  No se encontraron credenciales de Firebase.")
    print("📝 Configura una de estas opciones:")
    print("   1. Archivo: firebase-credentials.json")
    print("   2. Variables de entorno (ver .env.example)")
    print("   3. Editar config.py manualmente")
    return False

def test_api():
    """Probar que la API funciona"""
    print("🚀 Probando API...")
    try:
        # Importar aquí para evitar errores si no está configurado
        from main import app
        print("✅ API se importa correctamente")
        print(f"📚 Documentación: http://localhost:{os.getenv('PORT', 8000)}/docs")
        return True
    except Exception as e:
        print(f"❌ Error en la API: {e}")
        return False

def main():
    """Función principal del setup"""
    print("🎯 Configuración de TradeJournal API")
    print("=" * 50)

    steps = [
        ("Dependencias", check_requirements),
        ("Configuración", create_config),
        ("Firebase", check_firebase_credentials),
        ("API", test_api)
    ]

    all_passed = True
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}:")
        if not step_func():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡Configuración completada exitosamente!")
        print("💡 Para ejecutar: python run.py")
        print("🌐 API: http://localhost:8000")
        print("📚 Docs: http://localhost:8000/docs")
    else:
        print("⚠️  Configuración incompleta. Revisa los errores arriba.")
        print("💡 Consulta el README.md para instrucciones detalladas.")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
