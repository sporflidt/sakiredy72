const Product = require("../../models/Product");

// Responsable: Integrante 1
const productResolvers = {
  Query: {
    products: async () => {
      return await Product.find().sort({ createdAt: -1 });
    },
    product: async (_, { id }) => {
      return await Product.findById(id);
    },
  },

  Mutation: {
    createProduct: async (_, { input }) => {
      const product = new Product(input);
      return await product.save();
    },

    updateProduct: async (_, { id, input }) => {
      const updated = await Product.findByIdAndUpdate(id, input, {
        new: true,
        runValidators: true,
      });
      if (!updated) throw new Error("Producto no encontrado");
      return updated;
    },

    deleteProduct: async (_, { id }) => {
      const deleted = await Product.findByIdAndDelete(id);
      return !!deleted;
    },
  },
};

module.exports = productResolvers;
