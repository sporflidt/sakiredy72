const mongoose = require("mongoose");

/**
 * Conexión a la base de datos MongoDB.
 * Usa MONGO_URI del .env (local con MongoDB Community/Compass,
 * o una cadena de MongoDB Atlas en la nube).
 */
const connectDB = async () => {
  try {
    const uri = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/graphql_class_db";
    await mongoose.connect(uri);
    console.log(`✅ MongoDB conectado: ${mongoose.connection.host}`);
  } catch (error) {
    console.error("❌ Error al conectar a MongoDB:", error.message);
    process.exit(1);
  }
};

module.exports = connectDB;
