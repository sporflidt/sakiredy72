const { Schema, model } = require("mongoose");

/**
 * ENTIDAD: Producto
 * Responsable: Integrante 1 (ejemplo)
 */
const ProductSchema = new Schema(
  {
    name: { type: String, required: true, trim: true },
    description: { type: String, trim: true },
    price: { type: Number, required: true, min: 0 },
    stock: { type: Number, required: true, default: 0 },
  },
  { timestamps: true }
);

module.exports = model("Product", ProductSchema);
