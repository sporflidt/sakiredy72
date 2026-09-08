const { Schema, model } = require("mongoose");

/**
 * ENTIDAD: Categoría
 * Responsable: Integrante 2 (ejemplo)
 */
const CategorySchema = new Schema(
  {
    name: { type: String, required: true, trim: true, unique: true },
    products: [{ type: Schema.Types.ObjectId, ref: "Product" }],
  },
  { timestamps: true }
);

module.exports = model("Category", CategorySchema);
