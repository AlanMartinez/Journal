#!/usr/bin/env python3
"""
Script específico para configurar Firebase con las credenciales correctas
"""

import json
import os
import webbrowser

def show_firebase_instructions():
    """Mostrar instrucciones paso a paso"""
    print("🔥 Configuración de Firebase para TradeJournal API")
    print("=" * 60)

    print("\n📝 IMPORTANTE: Las keys que tienes son para el CLIENTE web,")
    print("   pero necesitas credenciales de SERVIDOR (Service Account)")

    print("\n🚀 PASOS PARA OBTENER CREDENCIALES DE SERVIDOR:")
    print("\n1️⃣  Ve a: https://console.firebase.google.com/project/tradejournal-9075d/settings/serviceaccounts/adminsdk")

    print("\n2️⃣  En la sección 'Service accounts', haz clic en 'Generate new private key'")

    print("\n3️⃣  Descarga el archivo JSON (se llama algo como 'tradejournal-9075d-firebase-adminsdk-xxxxx.json')")

    print("\n4️⃣  Renombra el archivo descargado a: firebase-credentials.json")

    print("\n5️⃣  Colócalo en la carpeta: API/firebase-credentials.json")

    print("\n📝 Configura el database_id (opcional):")
    print("   - En config.py: FIREBASE_DATABASE_ID = 'journal-db'")
    print("   - O variable de entorno: export FIREBASE_DATABASE_ID='journal-db'")
    print("   - Por defecto usa: '(default)'")

    print("\n📋 Una vez que tengas el archivo correcto, debería verse así:")
    print('''
{
  "type": "service_account",
  "project_id": "tradejournal-9075d",
  "private_key_id": "real-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@tradejournal-9075d.iam.gserviceaccount.com",
  "client_id": "real-client-id",
  ...
}
    ''')

def check_current_setup():
    """Verificar configuración actual"""
    print("\n🔍 Verificando configuración actual...")

    # Verificar si existe el archivo de credenciales
    cred_file = 'firebase-credentials.json'
    if os.path.exists(cred_file):
        try:
            with open(cred_file, 'r') as f:
                data = json.load(f)

            # Verificar si tiene las credenciales correctas
            if data.get('private_key_id') != 'your-private-key-id':
                print(f"✅ Archivo de credenciales encontrado: {cred_file}")
                print("✅ Parece tener credenciales válidas")
                return True
            else:
                print(f"⚠️  Archivo encontrado pero con credenciales de ejemplo: {cred_file}")
                return False
        except json.JSONDecodeError:
            print(f"❌ Archivo de credenciales inválido: {cred_file}")
            return False
    else:
        print(f"❌ No se encontró archivo de credenciales: {cred_file}")
        return False

def open_firebase_console():
    """Abrir Firebase Console en el navegador"""
    print("\n🌐 Abriendo Firebase Console...")
    webbrowser.open('https://console.firebase.google.com/project/tradejournal-9075d/settings/serviceaccounts/adminsdk')

def main():
    """Función principal"""
    print("🎯 Setup de Firebase para tu proyecto tradejournal-9075d")
    print("=" * 60)

    # Mostrar instrucciones
    show_firebase_instructions()

    # Verificar configuración actual
    is_configured = check_current_setup()

    if not is_configured:
        print("\n❓ ¿Ya descargaste el archivo de credenciales?")
        response = input("   (s/n): ").lower().strip()

        if response == 's':
            print("\n📝 Renombra el archivo descargado a: firebase-credentials.json")
            print("   y colócalo en esta carpeta (API/)")
        else:
            print("\n🔗 ¿Quieres que abra Firebase Console para descargar las credenciales?")
            response = input("   (s/n): ").lower().strip()

            if response == 's':
                open_firebase_console()
                print("\n📋 Sigue las instrucciones en la consola de Firebase")
                print("   y luego renombra el archivo a: firebase-credentials.json")

    # Verificar configuración después
    print("\n🔄 Verificando de nuevo...")
    is_configured = check_current_setup()

    if is_configured:
        print("\n🎉 ¡Firebase configurado correctamente!")
        print("💡 Ahora puedes ejecutar: python run.py")
        print("🌐 La API estará disponible en: http://localhost:8000")
    else:
        print("\n⚠️  Firebase aún no está configurado correctamente.")
        print("💡 Completa los pasos anteriores y ejecuta este script de nuevo.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
