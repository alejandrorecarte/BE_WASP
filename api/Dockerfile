# Usa la imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /api/app

# Copia el archivo requirements.txt a la carpeta de trabajo
COPY api/app/requirements.txt /api/app/ 

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r /api/app/requirements.txt

# Copia todo el contenido de la carpeta 'app' al contenedor
COPY api/app/ /api/app/

# Expone el puerto en el que FastAPI estará corriendo
EXPOSE 8000

# Comando para ejecutar FastAPI usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
