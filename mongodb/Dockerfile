# Use the official MongoDB image from the Docker Hub
FROM mongo:latest

# Expose the default MongoDB port
EXPOSE 27017

# Copy the initialization script to the Docker container
COPY ./init-mongo.js /docker-entrypoint-initdb.d/

# Run the MongoDB server
CMD ["mongod"]