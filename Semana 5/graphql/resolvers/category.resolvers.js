const Category = require("../../models/Category");
const Product = require("../../models/Product");

// Responsable: Integrante 2
const categoryResolvers = {
  Query: {
    categories: async () => {
      return await Category.find().populate("products");
    },
    category: async (_, { id }) => {
      return await Category.findById(id).populate("products");
    },
  },

  Mutation: {
    createCategory: async (_, { input }) => {
      const category = new Category({
        name: input.name,
        products: input.productIds || [],
      });
      return await category.save();
    },

    addProductToCategory: async (_, { categoryId, productId }) => {
      const [category, product] = await Promise.all([
        Category.findById(categoryId),
        Product.findById(productId),
      ]);
      if (!category) throw new Error("Categoría no encontrada");
      if (!product) throw new Error("Producto no encontrado");

      if (!category.products.includes(productId)) {
        category.products.push(productId);
        await category.save();
      }
      return await category.populate("products");
    },

    deleteCategory: async (_, { id }) => {
      const deleted = await Category.findByIdAndDelete(id);
      return !!deleted;
    },
  },

  // Resolver de campo: resuelve "products" dentro de Category
  Category: {
    products: async (parent) => {
      // Si ya viene populado (populate), Mongoose devuelve los documentos completos
      if (parent.products && parent.products.length && parent.products[0].name) {
        return parent.products;
      }
      return await Product.find({ _id: { $in: parent.products } });
    },
  },
};

module.exports = categoryResolvers;
