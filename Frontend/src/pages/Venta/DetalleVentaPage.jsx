import { useState, useEffect } from "react";
import axios from "axios";
import "../../styles/detalle_venta.css";
import AutoInput from "../../components/AutoInput";

export default function DetalleVentaPage() {
  const [ventas, setVentas] = useState([]);
  const [factura, setFactura] = useState(null);

  const [form, setForm] = useState({
    id_venta: "",
    producto: "",
    cantidad: 1,
  });

  // ================================
  // CARGAR VENTAS
  // ================================
  useEffect(() => {
    axios
      .get("http://localhost:8000/venta/obtener/mes")
      .then((res) => setVentas(res.data))
      .catch(() => setVentas([]));
  }, []);

  // ================================
  // CARGAR FACTURA
  // ================================
  const cargarFactura = async (id) => {
    if (!id) return;

    try {
      const res = await axios.get(
        "http://localhost:8000/venta/factura/" + id
      );
      setFactura(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // ================================
  // AGREGAR DETALLE
  // ================================
  const agregarDetalle = async () => {
    if (!form.id_venta || !form.producto)
      return alert("Complete los datos.");

    try {
      await axios.post("http://localhost:8000/DetalleVenta/Create", form);

      cargarFactura(form.id_venta); // actualiza factura
      setForm({ ...form, producto: "", cantidad: 1 });

    } catch (err) {
      alert(err.response?.data?.detail || "Error al agregar producto");
    }
  };

  // ================================
  // ELIMINAR DETALLE
  // ================================
const eliminarProducto = async (idDetalle) => {
  if (!window.confirm("¿Eliminar este producto de la factura?")) return;

  try {
    await axios.delete(
      `http://localhost:8000/DetalleVenta/eliminar/${idDetalle}`
    );

    cargarFactura(form.id_venta); // Recarga la factura
  } catch (err) {
    console.log(err);
    alert("Error al eliminar: " + (err.response?.data?.detail || "Error desconocido"));
  }
};

  return (
    <div className="detalle-wrapper">
      <h2 className="detalle-title">Registrar Detalle de Venta</h2>

      <div className="detalle-grid">

        {/* ===================================================
              IZQUIERDA: FORMULARIO
        =================================================== */}
        <div className="detalle-left">

          <div className="section-title">Seleccionar Venta</div>
          <select
            className="form-input"
            onChange={(e) => {
              setForm({ ...form, id_venta: e.target.value });
              cargarFactura(e.target.value);
            }}
          >
            <option value="">Seleccione una venta</option>
            {ventas.map((v) => (
              <option key={v.id_venta} value={v.id_venta}>
                {v.cliente.nombre} — {v.fecha}
              </option>
            ))}
          </select>

          <div className="section-title">Producto</div>
          <AutoInput
            endpoint="Producto/autocompletado"
            value={form.producto}
            onChange={(v) => setForm({ ...form, producto: v })}
          />

          <div className="section-title">Cantidad</div>
          <input
            type="number"
            className="form-input"
            value={form.cantidad}
            min="1"
            onChange={(e) =>
              setForm({ ...form, cantidad: parseInt(e.target.value) })
            }
          />

          <button className="btn-primary" onClick={agregarDetalle}>
            Agregar a Factura
          </button>
        </div>

        {/* ===================================================
              DERECHA: FACTURA PROFESIONAL
        =================================================== */}
        <div className="detalle-right">
          <div className="invoice-box">

            {!factura ? (
              <p className="invoice-empty">
                Seleccione una venta para ver su factura.
              </p>
            ) : (
              <>
                {/* ================= Encabezado ================= */}
                <div className="invoice-header">
                  <h2>Factura</h2>
                  <span className="invoice-number">Venta #{factura.id_venta}</span>
                </div>

                {/* ================= Datos ================= */}
                <div className="invoice-info">
                  <p><strong>Cliente:</strong> {factura.cliente}</p>
                  <p><strong>Empleado:</strong> {factura.empleado}</p>
                  <p><strong>Fecha:</strong> {factura.fecha}</p>
                </div>

                {/* ================= Lista de Productos ================= */}
                <table className="invoice-table">
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th>Cant</th>
                      <th>Precio</th>
                      <th>Subtotal</th>
                      <th></th>
                    </tr>
                  </thead>

                  <tbody>
                    {factura.detalles.map((d) => (
                      <tr key={d.id_dv}>
                        <td>{d.producto}</td>
                        <td>{d.cantidad}</td>
                        <td>${d.precio_unit}</td>
                        <td>${d.sub_total}</td>
                        <td>
                          <button
                            className="delete-btn"
                            onClick={() => eliminarProducto(d.id_dv)}
                          >
                            ✖
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {/* ================= TOTAL ================= */}
                <div className="invoice-total">
                  <span>Total:</span>
                  <strong>${factura.total}</strong>
                </div>

                {/* ================= BOTÓN IMPRIMIR ================= */}
                <button className="print-btn" onClick={() => window.print()}>
                  🖨️ Imprimir Factura
                </button>
              </>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}
