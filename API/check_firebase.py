#!/usr/bin/env python3
"""
Script simple para verificar configuración de Firebase
"""

import json
import os

def check_firebase_credentials():
    """Verificar si Firebase está configurado correctamente"""
    print("🔥 Verificando configuración de Firebase...")
    print("=" * 50)

    # Verificar archivo de credenciales
    cred_file = 'firebase-credentials.json'
    if os.path.exists(cred_file):
        try:
            with open(cred_file, 'r') as f:
                data = json.load(f)

            print(f"✅ Archivo encontrado: {cred_file}")

            # Verificar campos requeridos
            required_fields = [
                'type', 'project_id', 'private_key_id',
                'private_key', 'client_email', 'client_id'
            ]

            missing_fields = []
            placeholder_fields = []

            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
                elif data[field] in ['your-private-key-id', 'your-client-id', '[REEMPLAZAR_CON_TU_PRIVATE_KEY_ID]', '[REEMPLAZAR_CON_TU_CLIENT_ID]']:
                    placeholder_fields.append(field)

            if missing_fields:
                print(f"❌ Campos faltantes: {', '.join(missing_fields)}")
                return False

            if placeholder_fields:
                print(f"⚠️  Campos con valores de ejemplo: {', '.join(placeholder_fields)}")
                print("   Reemplaza estos valores con los del archivo descargado de Firebase")
                return False

            print("✅ Todas las credenciales parecen válidas")
            return True

        except json.JSONDecodeError:
            print(f"❌ Archivo JSON inválido: {cred_file}")
            return False
    else:
        print(f"❌ No se encontró: {cred_file}")
        print("💡 Descarga las credenciales desde Firebase Console:")
        print("   https://console.firebase.google.com/project/tradejournal-9075d/settings/serviceaccounts/adminsdk")
        return False

def test_firebase_connection():
    """Probar conexión con Firebase"""
    print("\n🌐 Probando conexión con Firebase...")

    try:
        from app.services.database.firebase_service import FirebaseService
        service = FirebaseService("test")

        # Intentar una operación simple
        count = service.db.collection("test").limit(1).stream()
        list(count)  # Consumir el stream

        print("✅ Conexión con Firebase exitosa")
        return True

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verifica que las credenciales sean correctas")
        return False

def main():
    """Función principal"""
    print("🎯 Verificación de Firebase para TradeJournal")

    # Verificar credenciales
    credentials_ok = check_firebase_credentials()

    if credentials_ok:
        # Probar conexión
        connection_ok = test_firebase_connection()

        if connection_ok:
            print("\n🎉 ¡Firebase configurado correctamente!")
            print("💡 Puedes ejecutar ahora: python run.py")
        else:
            print("\n⚠️  Credenciales presentes pero error de conexión.")
            print("💡 Verifica que el proyecto Firebase esté activo.")
    else:
        print("\n📝 Para configurar Firebase:")
        print("1. Ve a: https://console.firebase.google.com/project/tradejournal-9075d/settings/serviceaccounts/adminsdk")
        print("2. Genera 'new private key'")
        print("3. Renombra el archivo a: firebase-credentials.json")
        print("4. Colócalo en esta carpeta (API/)")
        print("5. Ejecuta este script de nuevo")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
