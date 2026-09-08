const { mergeTypeDefs } = require("@graphql-tools/merge");

const productTypeDefs = require("./product.typeDefs");
const categoryTypeDefs = require("./category.typeDefs");

/**
 * Cada integrante agrega aquí el typeDefs de su entidad.
 * mergeTypeDefs combina automáticamente los bloques Query/Mutation
 * de cada archivo en un único schema.
 */
const typeDefs = mergeTypeDefs([
  productTypeDefs,
  categoryTypeDefs,
  // agregar aquí el typeDefs de nuevas entidades del equipo...
]);

module.exports = typeDefs;
