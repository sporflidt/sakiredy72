const { gql } = require("apollo-server-express");

// Responsable: Integrante 1
const productTypeDefs = gql`
  type Product {
    id: ID!
    name: String!
    description: String
    price: Float!
    stock: Int!
    createdAt: String
    updatedAt: String
  }

  input ProductInput {
    name: String!
    description: String
    price: Float!
    stock: Int
  }

  input ProductUpdateInput {
    name: String
    description: String
    price: Float
    stock: Int
  }

  type Query {
    products: [Product!]!
    product(id: ID!): Product
  }

  type Mutation {
    createProduct(input: ProductInput!): Product!
    updateProduct(id: ID!, input: ProductUpdateInput!): Product!
    deleteProduct(id: ID!): Boolean!
  }
`;

module.exports = productTypeDefs;
