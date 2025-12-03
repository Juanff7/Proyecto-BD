import { useState, useEffect } from "react";
import axios from "axios";
import "../../styles/ventas.css";
import AutoInput from "../../components/AutoInput";

export default function GenerarVentaPage() {
  const [form, setForm] = useState({
    cliente: "",
    empleado: "",
  });

  const [preview, setPreview] = useState({
    cliente: "—",
    empleado: "—",
    total: 0,
    fecha: new Date().toLocaleString(),
  });

  const [historial, setHistorial] = useState([]);

  // Cargar ventas del mes
  useEffect(() => {
    axios.get("http://localhost:8000/venta/obtener/mes")
      .then(res => setHistorial(res.data))
      .catch(() => setHistorial([]));
  }, []);

  // Actualizar vista previa al escribir
  useEffect(() => {
    setPreview({
      ...preview,
      cliente: form.cliente || "—",
      empleado: form.empleado || "—",
    });
  }, [form]);

  // Crear Venta
  const crearVenta = async () => {
    try {
      const res = await axios.post("http://localhost:8000/venta/create", form);
      alert("Venta creada correctamente");
    } catch {
      alert("Error al crear venta");
    }
  };

  return (
    <div className="venta-wrapper">
      
      <h2 className="venta-title">Generar Nueva Venta</h2>

      <div className="venta-grid">

        {/* =================== COLUMNA IZQUIERDA =================== */}
        <div className="venta-form-card">

          <label className="form-label">Cliente</label>
          <AutoInput
            endpoint="Cliente/autocompletado"
            value={form.cliente}
            onChange={(v) => setForm({ ...form, cliente: v })}
          />

          <label className="form-label">Empleado</label>
          <AutoInput
            endpoint="Empleado/autocompletado"
            value={form.empleado}
            onChange={(v) => setForm({ ...form, empleado: v })}
          />

          <button className="btn-primary" onClick={crearVenta}>
            Crear Venta
          </button>
        </div>

        {/* =================== COLUMNA DERECHA =================== */}
        <div>
          <h3 className="historial-title">Ventas del Mes</h3>

          <div className="historial-box">
            {historial.length === 0 && (
              <p style={{ opacity: 0.5 }}>Aún no hay ventas este mes.</p>
            )}

            {historial.map((v, i) => (
              <div className="historial-item" key={i}>
              <div className="item-producto">{v.cliente.nombre}</div>
               <div className="item-mini">Empleado: {v.empleado.nombre}</div>

                <div className="item-mini">Fecha: {v.fecha}</div>
                <div className="item-total">Total: ${v.total}</div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* =================== VISTA PREVIA =================== */}
      <div className="preview-card">
        <div className="preview-title">Vista Previa</div>

        <div className="preview-line">Cliente: {preview.cliente}</div>
        <div className="preview-line">Empleado: {preview.empleado}</div>
        <div className="preview-line">Fecha: {preview.fecha}</div>

        <div className="preview-total">TOTAL: $0.00</div>
      </div>

    </div>
  );
}
