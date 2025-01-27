const dbName = process.env.MONGO_INITDB_DATABASE;
const dbUser = process.env.MONGO_INITDB_ROOT_USERNAME;
const dbPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;

print(`!!!!!!!!!!: dbName: ${dbName}`, `dbUser: ${dbUser}`, `dbPassword: ${dbPassword}`);
db = db.getSiblingDB(dbName);

// Eliminar la base de datos si ya existe
db.dropDatabase();

// Crear el usuario
db.createUser({
  user: dbUser,
  pwd: dbPassword,
  roles: [{ role: 'readWrite', db: dbName }]
});

// Crear la colección
db.createCollection('users');