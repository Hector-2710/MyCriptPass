# 1. Usar una imagen base oficial de Python (ligera)
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias al contenedor
COPY requirements.txt .

# 4. Instalar las dependencias
# --no-cache-dir mantiene la imagen pequeña
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de tu proyecto al contenedor
COPY . .

# 6. Exponer el puerto donde correrá la aplicación (informativo)
EXPOSE 80

# 7. Comando para ejecutar la aplicación
# Importante: host 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
