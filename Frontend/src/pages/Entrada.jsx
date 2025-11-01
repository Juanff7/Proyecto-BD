import { useState, useEffect } from "react";
import axios from "axios";

function Entrada() {
  const [detalle, setDetalle] = useState("");
  const [precioUnit, setPrecioU] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [producto, setProducto] = useState("");
  const [proveedor, setProveedor] = useState("");
  const [empleado, setEmpleado] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [productos, setProductos] = useState([]);

  // 🔹 Cargar productos al montar el componente
  useEffect(() => {
    axios
      .get("http://localhost:8000/Producto/")
      .then((res) => setProductos(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post("http://localhost:8000/Entrada/Create", {
        detalle,
        precio_unit: parseFloat(precioUnit),
        cantidad: parseInt(cantidad),
        producto,
        proveedor,
        empleado,
        fecha_ingreso: new Date().toISOString(),
      });

      console.log(res.data);
      setMensaje("✅ Registro creado correctamente");
      e.target.reset();
    } catch (error) {
      console.error(error);
      setMensaje("❌ Error al crear el registro");
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-6 text-white">
      {/* FORMULARIO */}
      <div className="bg-gray-900 shadow-lg rounded-xl p-8 w-full max-w-2xl mb-8 border border-gray-700">
        <h1 className="text-3xl font-bold text-center text-blue-400 mb-6">
          Crear Entrada de Proveedor
        </h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Detalle"
            onChange={(e) => setDetalle(e.target.value)}
            className="col-span-2 bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="number"
            placeholder="Precio Unitario"
            onChange={(e) => setPrecioU(e.target.value)}
            className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="number"
            placeholder="Cantidad"
            onChange={(e) => setCantidad(e.target.value)}
            className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Producto"
            onChange={(e) => setProducto(e.target.value)}
            className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Proveedor"
            onChange={(e) => setProveedor(e.target.value)}
            className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Empleado"
            onChange={(e) => setEmpleado(e.target.value)}
            className="bg-gray-800 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            className="col-span-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
          >
            Registrar Entrada
          </button>
        </form>

        {mensaje && (
          <p
            className={`mt-4 text-center font-medium ${
              mensaje.includes("✅") ? "text-green-400" : "text-red-400"
            }`}
          >
            {mensaje}
          </p>
        )}
      </div>

      {/* TABLA DE PRODUCTOS */}
      <div className="bg-gray-900 shadow-lg rounded-xl p-6 w-full max-w-5xl border border-gray-700 overflow-x-auto">
        <h2 className="text-2xl font-bold text-blue-400 mb-4 text-center">
          Productos Disponibles
        </h2>
        <table className="min-w-full border border-gray-700 text-sm">
          <thead className="bg-gray-800 text-blue-300">
            <tr>
              <th className="border border-gray-700 px-4 py-2">ID</th>
              <th className="border border-gray-700 px-4 py-2">Nombre</th>
              <th className="border border-gray-700 px-4 py-2">Descripción</th>
              <th className="border border-gray-700 px-4 py-2">Costo Venta</th>
              <th className="border border-gray-700 px-4 py-2">Cantidad</th>
              <th className="border border-gray-700 px-4 py-2">Categoría</th>
              <th className="border border-gray-700 px-4 py-2">Imagen</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((p) => (
              <tr key={p.id} className="hover:bg-gray-800 transition">
                <td className="border border-gray-700 px-4 py-2">{p.id}</td>
                <td className="border border-gray-700 px-4 py-2">{p.nombre}</td>
                <td className="border border-gray-700 px-4 py-2">{p.descripcion}</td>
                <td className="border border-gray-700 px-4 py-2">{p.costo_venta}</td>
                <td className="border border-gray-700 px-4 py-2">{p.cantidad}</td>
                <td className="border border-gray-700 px-4 py-2">{p.categoria?.tipo}</td>
                <td className="border border-gray-700 px-4 py-2 text-center">
                  {p.imagen_url ? (
                    <img
                      src={p.imagen_url}
                      alt={p.nombre}
                      className="w-16 h-16 object-cover mx-auto rounded-md"
                    />
                  ) : (
                    "Sin imagen"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Entrada;
