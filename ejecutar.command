#!/bin/bash
# Doble clic en Mac, o ./ejecutar.command en Linux/Mac
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "No encuentro python3. Instalalo desde https://www.python.org/downloads/"
    read -r -p "Enter para salir"; exit 1
fi

if [ ! -d .venv ]; then
    echo "Creando entorno virtual e instalando dependencias..."
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
else
    source .venv/bin/activate
fi

python tijera_fuerzas.py "$@"
echo
read -r -p "Enter para cerrar"
