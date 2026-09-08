const { gql } = require("apollo-server-express");

// Responsable: Integrante 2
const categoryTypeDefs = gql`
  type Category {
    id: ID!
    name: String!
    products: [Product!]!
    createdAt: String
    updatedAt: String
  }

  input CategoryInput {
    name: String!
    productIds: [ID!]
  }

  type Query {
    categories: [Category!]!
    category(id: ID!): Category
  }

  type Mutation {
    createCategory(input: CategoryInput!): Category!
    addProductToCategory(categoryId: ID!, productId: ID!): Category!
    deleteCategory(id: ID!): Boolean!
  }
`;

module.exports = categoryTypeDefs;
