# Proyecto GraphQL + Express + MongoDB (Apollo Server)

Backend GraphQL construido con **Express**, **Apollo Server 3** y **MongoDB/Mongoose**,
organizado para que cada integrante del equipo implemente su propia entidad
(typeDefs + resolvers) de forma independiente y sin pisarse el código.

## 1. Stack y versiones

| Paquete | Versión |
|---|---|
| express | 4.19.2 |
| cors | 2.8.5 |
| graphql | 15.10.1 |
| apollo-server-express | 3.13.0 |
| mongoose | 8.17.1 |
| nodemon | ^3.1.4 (dev) |

> Nota: `apollo-server-express@3.13.0` requiere `express@^4`, por eso se usa
> Express 4 (no 5) en este proyecto.

## 2. Instalación

```bash
git clone <url-del-repositorio>
cd graphql-mongo-project
npm install
```

Crear el archivo `.env` en la raíz (basado en `.env.example`):

```
PORT=4000
MONGO_URI=mongodb://127.0.0.1:27017/graphql_class_db
```

- Si usan **MongoDB Community + Compass** en local, no necesitan cambiar nada
  (solo tener el servicio `mongod` corriendo).
- Si usan **MongoDB Atlas** (nube), reemplacen `MONGO_URI` por la cadena de
  conexión que les da Atlas (`mongodb+srv://...`).

## 3. Levantar el servidor

```bash
npm start
```

Esto ejecuta `nodemon server.js`. Verán algo como:

```
✅ MongoDB conectado: 127.0.0.1
🚀 Servidor listo en http://localhost:4000/graphql
```

Abran `http://localhost:4000/graphql` en el navegador para usar el
**Apollo Sandbox** y probar Queries/Mutations.
