import { useState, useEffect } from "react";
import axios from "axios";
import "../../styles/compra.css";
import AutoInput from "../../components/AutoInput";

export default function GenerarCompra() {
  const [form, setForm] = useState({
    producto: "",
    precio_unit: "",
    cantidad: "",
    proveedor: "",
    empleado: "",
    detalle: "",
  });

  const [productoInfo, setProductoInfo] = useState(null); // Datos completos del producto
  const [historial, setHistorial] = useState([]); // Historial local

  // Cargar info del producto cuando cambia el nombre seleccionado
  useEffect(() => {
    if (!form.producto) {
      setProductoInfo(null);
      return;
    }

    const fetchProducto = async () => {
      try {
        const res = await axios.get("http://localhost:8000/Producto/");
        const lista = res.data;

        const encontrado = lista.find(
          (p) => p.nombre.toLowerCase() === form.producto.toLowerCase()
        );

        setProductoInfo(encontrado || null);
      } catch {
        setProductoInfo(null);
      }
    };

    fetchProducto();
  }, [form.producto]);

  // Calcular total
  const total = form.precio_unit && form.cantidad
    ? (parseFloat(form.precio_unit) * parseInt(form.cantidad)).toFixed(2)
    : "0.00";

  // Submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.producto || !form.proveedor || !form.empleado) {
      return alert("Producto, proveedor y empleado son obligatorios.");
    }

    try {
      await axios.post("http://localhost:8000/Entrada/Create", form);

      // Registrar en historial instantáneo
      setHistorial([
        {
          fecha: new Date().toLocaleString(),
          producto: form.producto,
          cantidad: form.cantidad,
          precio: form.precio_unit,
          total,
        },
        ...historial,
      ]);

      alert("Compra registrada correctamente.");

      setForm({
        producto: "",
        precio_unit: "",
        cantidad: "",
        proveedor: "",
        empleado: "",
        detalle: "",
      });

      setProductoInfo(null);
    } catch (error) {
      console.log(error);
      alert("Error al registrar la compra.");
    }
  };

  return (
    <div className="compra-wrapper">

      {/* ============================================== 
          CONTENEDOR EN DOS COLUMNAS
      =============================================== */}
      <div className="compra-grid">

        {/* ============================================== 
            1) COLUMNA IZQUIERDA — FORMULARIO
        =============================================== */}
        <div className="columna-form">

          <h2 className="Title">Registrar Compra</h2>

          <form onSubmit={handleSubmit} className="compra-form">

            <h3 className="section-title">Producto</h3>
            <AutoInput
              label="Producto:"
              endpoint="Producto/autocompletado"
              value={form.producto}
              onChange={(v) => setForm({ ...form, producto: v })}
            />

            <label className="form-label">Precio unitario</label>
            <input
              type="number"
              className="form-input"
              value={form.precio_unit}
              onChange={(e) =>
                setForm({ ...form, precio_unit: e.target.value })
              }
            />

            <label className="form-label">Cantidad</label>
            <input
              type="number"
              className="form-input"
              value={form.cantidad}
              onChange={(e) =>
                setForm({ ...form, cantidad: e.target.value })
              }
            />

            <h3 className="section-title">Proveedor</h3>
            <AutoInput
              label="Proveedor:"
              endpoint="Proveedor/autocompletado"
              value={form.proveedor}
              onChange={(v) => setForm({ ...form, proveedor: v })}
            />

            <h3 className="section-title">Empleado</h3>
            <AutoInput
              label="Empleado:"
              endpoint="Empleado/autocompletado"
              value={form.empleado}
              onChange={(v) => setForm({ ...form, empleado: v })}
            />

            <h3 className="section-title">Detalle (Opcional)</h3>
            <textarea
              className="form-textarea"
              value={form.detalle}
              onChange={(e) => setForm({ ...form, detalle: e.target.value })}
            />

            <button type="submit" className="btn-primary">Registrar compra</button>
          </form>

        </div>

        {/* ============================================== 
            2) COLUMNA DERECHA — RESUMEN
        =============================================== */}
        <div className="columna-resumen">

          <h3 className="resumen-title">Resumen</h3>

          <div className="resumen-card">
            {productoInfo ? (
              <>
                {productoInfo.imagen_url && (
                  <img
                    src={productoInfo.imagen_url}
                    className="resumen-img"
                    alt="producto"
                  />
                )}

                <p><strong>Nombre:</strong> {productoInfo.nombre}</p>
                <p><strong>Stock actual:</strong> {productoInfo.cantidad}</p>
                <p><strong>Precio venta:</strong> ${productoInfo.costo_venta}</p>
                <hr />
              </>
            ) : (
              <p className="resumen-placeholder">Selecciona un producto</p>
            )}

            <p><strong>Precio unitario:</strong> ${form.precio_unit || "0.00"}</p>
            <p><strong>Cantidad:</strong> {form.cantidad || "0"}</p>

            <p className="resumen-total">
              TOTAL: ${total}
            </p>

            <hr />

            <p><strong>Proveedor:</strong> {form.proveedor || "—"}</p>
            <p><strong>Empleado:</strong> {form.empleado || "—"}</p>
          </div>

          {/* HISTORIAL */}
          <h3 className="resumen-title">Historial reciente</h3>
          <div className="historial-box">
            {historial.length === 0 ? (
              <p className="historial-placeholder">No hay compras recientes.</p>
            ) : (
              historial.slice(0, 5).map((h, i) => (
                <div key={i} className="historial-item">
                  <span>{h.fecha}</span>
                  <strong>{h.producto}</strong>
                  <span>{h.cantidad} und — ${h.precio}</span>
                  <span>Total: ${h.total}</span>
                </div>
              ))
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
