import { useState, useEffect } from "react";
import axios from "axios";
import "../../styles/RegistrarPrecio.css";

const API_H = "http://localhost:8000/Historial/create";
const API_P = "http://localhost:8000/Producto/autocompletado";
const API_PRODUCTO = "http://localhost:8000/Producto";

export default function RegistrarCambioPrecio() {
  const [busqueda, setBusqueda] = useState("");
  const [sugerencias, setSugerencias] = useState([]);

  const [productoSeleccionado, setProductoSeleccionado] = useState(null);
  const [precioActual, setPrecioActual] = useState("");
  const [precioNuevo, setPrecioNuevo] = useState("");

  const [loading, setLoading] = useState(false);

  // ===============================
  // AUTOCOMPLETADO
  // ===============================
  const buscarProducto = async (query) => {
    if (!query.trim()) return setSugerencias([]);

    const res = await axios.get(`${API_P}?query=${query}`);
    setSugerencias(res.data);
  };

  const seleccionarProducto = async (p) => {
    setBusqueda(p.nombre);
    setSugerencias([]);

    const res = await axios.get(`${API_PRODUCTO}/${p.id_producto}`);

    setProductoSeleccionado(res.data);
    setPrecioActual(res.data.costo_venta);
  };

  // ===============================
  // GUARDAR CAMBIO DE PRECIO
  // ===============================
  const guardarCambio = async () => {
    if (!productoSeleccionado)
      return alert("Seleccione un producto.");

    if (!precioNuevo || precioNuevo <= 0)
      return alert("Ingrese un precio válido.");

    const data = {
      producto: productoSeleccionado.id_producto,
      precio_nuevo: Number(precioNuevo),
      fecha_de_cambio: new Date().toISOString(),
    };

    try {
      setLoading(true);
      await axios.post(API_H, data);

      alert("Cambio de precio registrado exitosamente.");

      setPrecioNuevo("");
      setProductoSeleccionado(null);
      setBusqueda("");
      setPrecioActual("");
    } catch (err) {
      console.log(err);
      alert("Error al registrar cambio de precio.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rp-container">
      <h1 className="rp-title">Registrar Cambio de Precio</h1>

      <div className="rp-card">

        {/* BUSCADOR */}
        <label>Buscar Producto</label>
        <input
          className="rp-input"
          placeholder="Ej: Bate Mizuno..."
          value={busqueda}
          onChange={(e) => {
            setBusqueda(e.target.value);
            buscarProducto(e.target.value);
          }}
        />

        {/* AUTOCOMPLETADO */}
        {sugerencias.length > 0 && (
          <div className="rp-suggest-box">
            {sugerencias.map((s) => (
              <div
                key={s.id_producto}
                className="rp-suggest-item"
                onClick={() => seleccionarProducto(s)}
              >
                {s.nombre}
              </div>
            ))}
          </div>
        )}

        {/* INFO PRODUCTO */}
        {productoSeleccionado && (
          <div className="rp-product-info">
            <h3>{productoSeleccionado.nombre}</h3>
            <p><strong>ID:</strong> {productoSeleccionado.id_producto}</p>
            <p><strong>Categoría:</strong> {productoSeleccionado.categoria?.tipo || "-"}</p>
            <p><strong>Precio Actual:</strong> ${precioActual}</p>
          </div>
        )}

        {/* NUEVO PRECIO */}
        {productoSeleccionado && (
          <>
            <label>Nuevo Precio</label>
            <input
              type="number"
              className="rp-input"
              placeholder="Nuevo precio..."
              value={precioNuevo}
              onChange={(e) => setPrecioNuevo(e.target.value)}
            />

            <button
              className="rp-btn"
              onClick={guardarCambio}
              disabled={loading}
            >
              {loading ? "Guardando..." : "Guardar Cambio"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
