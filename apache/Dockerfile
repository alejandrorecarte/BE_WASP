# Imagen base de Apache
FROM httpd:latest

# Establecer el directorio de trabajo donde estarán los archivos estáticos
WORKDIR /usr/local/apache2/htdocs/

# Copiar tus archivos estáticos (HTML, CSS, JS) al contenedor
COPY /apache /usr/local/apache2/htdocs/

# Asegurar que los archivos tienen los permisos correctos
RUN chmod -R 755 /usr/local/apache2/htdocs/

# Copiar configuración personalizada de Apache
COPY ./apache/conf/proxy.conf /usr/local/apache2/conf/extra/proxy.conf

# Habilitar los módulos necesarios de Apache para proxy
RUN echo "Include /usr/local/apache2/conf/extra/proxy.conf" >> /usr/local/apache2/conf/httpd.conf
RUN echo "LoadModule proxy_module modules/mod_proxy.so" >> /usr/local/apache2/conf/httpd.conf
RUN echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /usr/local/apache2/conf/httpd.conf
# Habilitar mod_rewrite
RUN echo "LoadModule rewrite_module modules/mod_rewrite.so" >> /usr/local/apache2/conf/httpd.conf

# Exponer el puerto 80 para Apache
EXPOSE 80

# Comando para iniciar Apache
CMD ["httpd-foreground"]
