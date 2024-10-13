#!/bin/bash
set -e

# Comandos de inicialización
echo "Iniciando el contenedor..."

# Iniciar Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=7860 --no-browser --allow-root --notebook-dir=/dli/task
