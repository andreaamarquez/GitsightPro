#!/bin/bash


# Comandos SQL para reiniciar el esquema de la base de datos
echo "Eliminando schema public..."
psql -U postgres -d datamining_db -a -f reset_schema.sql

# Eliminar config.json si existe
if [ -f config.json ]; then
    echo "Eliminando config.json..."
    rm config.json
fi

# Iniciar el servidor en segundo plano
echo "Iniciando el servidor..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Esperar hasta que config.json exista
while true; do
    if [ -f config.json ]; then
        if [ -n "$(cat config.json | grep 'gh_user')" ] && \
           [ -n "$(cat config.json | grep 'gh_token')" ] && \
           [ -n "$(cat config.json | grep 'owner')" ] && \
           [ -n "$(cat config.json | grep 'name')" ]; then
            break
        fi
    fi
    
    if [ "$(uname)" == "Darwin" ]; then
        # macOS (no es necesario el comando timeout)
        sleep 1
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Linux (utiliza el comando timeout)
        timeout 5 tail --pid=$! -f /dev/null
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
        # Windows (utiliza el comando timeout de Windows)
        timeout /t 5
    fi
done

# Cuando config.json existe, ejecutar data-abstraction.py
echo "Ejecutando data-abstraction.py..."
python data-abstraction.py
