#!/usr/bin/env python
"""
Script auxiliar para ejecutar los tests unitarios
"""
import sys
import subprocess
import os

def main():
    """Ejecutar los tests unitarios"""
    # Cambiar al directorio de la API
    api_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(api_dir)
    
    # Argumentos por defecto para pytest
    args = ['pytest', '-v', 'tests/']
    
    # Agregar argumentos adicionales si se proporcionan
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    
    # Ejecutar pytest
    result = subprocess.run(args)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()

