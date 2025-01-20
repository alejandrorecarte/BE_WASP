# Usa la imagen oficial de MariaDB como base
FROM mariadb:latest

# Establece el maintainer (opcional)
LABEL maintainer="alejandro.recarte.rebollo@gmail.com"

# Copia archivos de configuración personalizados (si tienes)
# Por ejemplo, podrías agregar un archivo de configuración custom para MariaDB
# COPY ./my.cnf /etc/mysql/my.cnf

COPY /mariadb/init.sql /docker-entrypoint-initdb.d/

# Copia scripts de inicialización, si tienes alguno
# Estos scripts se ejecutarán cuando el contenedor se inicie por primera vez
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto 3306 para conectarse al contenedor
EXPOSE 3306

# El contenedor usará el comando de entrada predeterminado de MariaDB
#CMD ["mysqld"]
