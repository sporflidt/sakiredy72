const productResolvers = require("./product.resolvers");
const categoryResolvers = require("./category.resolvers");

/**
 * Cada integrante agrega aquí el resolver de su entidad.
 * Se combinan los bloques Query y Mutation de todos los archivos,
 * y se mantienen aparte los "resolvers de campo" (ej: Category.products).
 */
const resolvers = {
  Query: {
    ...productResolvers.Query,
    ...categoryResolvers.Query,
    // ...agregar aquí Query de nuevas entidades
  },
  Mutation: {
    ...productResolvers.Mutation,
    ...categoryResolvers.Mutation,
    // ...agregar aquí Mutation de nuevas entidades
  },
  // Resolvers de campo por tipo (ej. relaciones entre entidades)
  Category: {
    ...categoryResolvers.Category,
  },
};

module.exports = resolvers;
