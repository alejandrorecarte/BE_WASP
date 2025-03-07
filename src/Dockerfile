# Usa la imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /src

# Crea un usuario no root y establece permisos
RUN useradd -m nonrootuser && chown -R nonrootuser /src

# Copia el archivo requirements.txt a la carpeta de trabajo
COPY requirements.txt /src

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r /src/requirements.txt

# Copia todo el contenido de la carpeta 'app' al contenedor
COPY src /src

# Cambia al usuario no root
USER nonrootuser

# Expone el puerto en el que FastAPI estará corriendo
EXPOSE 8000

# Comando para ejecutar FastAPI usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
