require("dotenv").config();

const express = require("express");
const cors = require("cors");
const { ApolloServer } = require("apollo-server-express");

const connectDB = require("./config/db");
const typeDefs = require("./graphql/typeDefs");
const resolvers = require("./graphql/resolvers");

async function startServer() {
  // 1. Conexión a la base de datos
  await connectDB();

  // 2. App Express
  const app = express();
  app.use(cors());
  app.use(express.json());

  // 3. Servidor Apollo (GraphQL) con Sandbox habilitado
  const apolloServer = new ApolloServer({
    typeDefs,
    resolvers,
    // El Sandbox de Apollo se activa automáticamente si NODE_ENV !== "production"
  });

  await apolloServer.start();
  apolloServer.applyMiddleware({ app, path: "/graphql" });

  // 4. Levantar servidor
  const PORT = process.env.PORT || 4000;
  app.listen(PORT, () => {
    console.log(`🚀 Servidor listo en http://localhost:${PORT}${apolloServer.graphqlPath}`);
  });
}

startServer().catch((err) => {
  console.error("Error al iniciar el servidor:", err);
});
