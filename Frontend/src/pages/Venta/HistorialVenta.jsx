import { useState, useEffect, useMemo } from "react";
import axios from "axios";
import "../../styles/HistorialVentas.css";
import * as XLSX from "xlsx";

const API_VENTA = "http://localhost:8000/venta";
const API_DETALLE = "http://localhost:8000/DetalleVenta";

export default function HistorialVentasPage() {
  const [ventas, setVentas] = useState([]);
  const [search, setSearch] = useState("");

  const [fecha, setFecha] = useState("");
  const [inicio, setInicio] = useState("");
  const [fin, setFin] = useState("");

  const [modalData, setModalData] = useState(null);

  const [page, setPage] = useState(1);
  const pageSize = 10;

  // =======================
  // CARGAR VENTAS + DETALLES
  // =======================
  const cargarVentas = async () => {
    try {
      // 1) Ventas
      const resVentas = await axios.get(`${API_VENTA}/obtener`);

      // 2) Todos los detalles de venta (para buscar por producto)
      let detallesPorVenta = {};
      try {
        const resDetalles = await axios.get(
          `${API_DETALLE}/obtener_todos`
        );
        detallesPorVenta = {};
        for (const d of resDetalles.data) {
          const idVenta = d.id_venta || d.venta?.id_venta;
          if (!idVenta) continue;
          if (!detallesPorVenta[idVenta]) detallesPorVenta[idVenta] = [];
          detallesPorVenta[idVenta].push(d);
        }
      } catch (err) {
        console.warn("No se pudieron cargar detalles de venta:", err);
      }

      // 3) Unir datos
      const ventasConDetalles = resVentas.data.map((v) => ({
        ...v,
        detalles: detallesPorVenta[v.id_venta] || [],
      }));

      setVentas(ventasConDetalles);
      setPage(1);
    } catch (err) {
      console.error(err);
      alert("Error al cargar ventas.");
    }
  };

  useEffect(() => {
    cargarVentas();
  }, []);

  // =======================
  // FILTRAR POR FECHA ÚNICA
  // =======================
  const filtrarFecha = async () => {
    try {
      if (!fecha) {
        return cargarVentas();
      }
      const res = await axios.get(`${API_VENTA}/buscar_fecha/${fecha}`);
      setVentas(res.data);
      setPage(1);
    } catch (err) {
      console.error(err);
      alert("Error al buscar por fecha.");
    }
  };

  // =======================
  // FILTRAR POR RANGO
  // =======================
  const filtrarRango = async () => {
    try {
      if (!inicio || !fin) return alert("Selecciona ambas fechas.");
      const res = await axios.get(`${API_VENTA}/rango`, {
        params: { inicio, fin },
      });
      setVentas(res.data);
      setPage(1);
    } catch (err) {
      console.error(err);
      alert("Error al filtrar por rango de fechas.");
    }
  };

  // =======================
  // BÚSQUEDA GLOBAL (cliente, empleado, producto)
  // =======================
  const filtrados = useMemo(
    () =>
      ventas.filter((v) => {
        const productosTexto = (v.detalles || [])
          .map((d) => d.producto?.nombre || d.producto || "")
          .join(" ");

        const texto = `
          ${v.cliente?.nombre || ""}
          ${v.empleado?.nombre || ""}
          ${productosTexto}
        `
          .toLowerCase()
          .replace(/\s+/g, " ");

        return texto.includes(search.toLowerCase().trim());
      }),
    [ventas, search]
  );

  // =======================
  // PAGINACIÓN
  // =======================
  const totalPages = Math.max(1, Math.ceil(filtrados.length / pageSize));
  const safePage = Math.min(page, totalPages);

  const dataPage = filtrados.slice(
    (safePage - 1) * pageSize,
    safePage * pageSize
  );

  const irPagina = (p) => {
    if (p >= 1 && p <= totalPages) setPage(p);
  };

  // =======================
  // TOP CLIENTES (HISTOGRAMA)
  // =======================
  const statsClientes = useMemo(() => {
    const mapa = new Map();
    for (const v of filtrados) {
      const n = v.cliente?.nombre || "Desconocido";
      const total = v.total || 0;
      mapa.set(n, (mapa.get(n) || 0) + total);
    }
    return [...mapa.entries()]
      .map(([cliente, total]) => ({ cliente, total }))
      .sort((a, b) => b.total - a.total);
  }, [filtrados]);

  const maxClienteTotal = statsClientes[0]?.total || 1;

  // =======================
  // EXPORTAR EXCEL
  // =======================
  const exportarExcel = () => {
    if (!filtrados.length) return alert("No hay datos para exportar.");

    const data = filtrados.map((v) => ({
      ID: v.id_venta,
      Cliente: v.cliente?.nombre || "",
      Empleado: v.empleado?.nombre || "",
      Fecha: new Date(v.fecha).toLocaleString(),
      Total: v.total || 0,
    }));

    const ws = XLSX.utils.json_to_sheet(data);

    ws["!cols"] = Object.keys(data[0]).map((key) => ({
      wch: key.length + 10,
    }));

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Ventas");

    XLSX.writeFile(wb, "Historial_Ventas.xlsx");
  };

  // =======================
  // EXPORTAR PDF
  // =======================
  const exportarPDF = async () => {
    if (!filtrados.length) return alert("No hay datos para el PDF.");

    const payload = {
      filtros: { search, fecha, inicio, fin },
      ventas: filtrados,
    };

    const res = await axios.post(`${API_VENTA}/reporte/general`, payload, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "reporte_ventas.pdf");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  // =======================
  // OBTENER FACTURA (MODAL)
  // =======================
  const verFactura = async (id) => {
    try {
      const res = await axios.get(`${API_VENTA}/factura/${id}`);
      setModalData(res.data);
    } catch (err) {
      console.error(err);
      alert("Error al cargar la factura.");
    }
  };

  const totalMonto = filtrados.reduce(
    (acc, v) => acc + (v.total || 0),
    0
  );

  return (
    <div className="hv-container">
      <h1 className="hv-title">Historial de Ventas</h1>

      {/* ===================== FILTROS ===================== */}
      <div className="hv-filtros">
        <input
          className="hv-input hv-input-wide"
          placeholder="Buscar cliente, empleado, producto..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="hv-filter-group">
          <label>Fecha</label>
          <div className="hv-filter-row">
            <input
              type="date"
              className="hv-input"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
            />
            <button className="hv-btn" onClick={filtrarFecha}>
              Buscar
            </button>
          </div>
        </div>

        <div className="hv-filter-group">
          <label>Rango</label>
          <div className="hv-filter-row">
            <input
              type="date"
              className="hv-input"
              value={inicio}
              onChange={(e) => setInicio(e.target.value)}
            />
            <input
              type="date"
              className="hv-input"
              value={fin}
              onChange={(e) => setFin(e.target.value)}
            />
            <button className="hv-btn" onClick={filtrarRango}>
              Aplicar
            </button>
          </div>
        </div>

        <div className="hv-filter-group">
          <label>Exportar</label>
          <div className="hv-filter-row">
            <button className="hv-btn-excel" onClick={exportarExcel}>
              Excel
            </button>
            <button className="hv-btn-pdf" onClick={exportarPDF}>
              PDF
            </button>
            <button className="hv-btn-secondary" onClick={cargarVentas}>
              Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* ===================== RESUMEN ===================== */}
      <div className="hv-summary">
        <div className="hv-card">
          <span className="hv-card-label">Ventas mostradas</span>
          <span className="hv-card-value">{filtrados.length}</span>
        </div>

        <div className="hv-card">
          <span className="hv-card-label">Monto total</span>
          <span className="hv-card-value">${totalMonto.toFixed(2)}</span>
        </div>

        {statsClientes[0] && (
          <div className="hv-card">
            <span className="hv-card-label">Cliente top</span>
            <span className="hv-card-value">
              {statsClientes[0].cliente}
            </span>
          </div>
        )}
      </div>

      {/* ===================== HISTOGRAMA CLIENTES ===================== */}
      <div className="hv-stats">
        <h2 className="hv-subtitle">Clientes por monto comprado</h2>

        {statsClientes.length === 0 ? (
          <p className="hv-empty">No hay datos.</p>
        ) : (
          <div className="hv-chart">
            {statsClientes.map((c) => (
              <div className="hv-bar" key={c.cliente}>
                <span className="hv-bar-label">
                  {c.cliente} — ${c.total.toFixed(2)}
                </span>
                <div className="hv-bar-track">
                  <div
                    className="hv-bar-fill"
                    style={{
                      width: `${(c.total / maxClienteTotal) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ===================== TABLA ===================== */}
      <div className="hv-table">
        <div className="hv-row hv-header">
          <span>ID</span>
          <span>Cliente</span>
          <span>Empleado</span>
          <span>Fecha</span>
          <span>Total</span>
          <span>Acciones</span>
        </div>

        {dataPage.map((v) => (
          <div className="hv-row" key={v.id_venta}>
            <span>{v.id_venta}</span>
            <span>{v.cliente?.nombre}</span>
            <span>{v.empleado?.nombre}</span>
            <span>{new Date(v.fecha).toLocaleString()}</span>
            <span>${v.total}</span>

            <div className="hv-actions">
              <button
                className="hv-btn-detalle"
                onClick={() => verFactura(v.id_venta)}
              >
                Ver
              </button>
            </div>
          </div>
        ))}

        {dataPage.length === 0 && (
          <div className="hv-row hv-empty-row">
            <span>No hay registros.</span>
          </div>
        )}
      </div>

      {/* ===================== PAGINACIÓN ===================== */}
      <div className="hv-pagination">
        <button onClick={() => irPagina(safePage - 1)}>«</button>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
          <button
            key={p}
            onClick={() => irPagina(p)}
            className={p === safePage ? "active" : ""}
          >
            {p}
          </button>
        ))}
        <button onClick={() => irPagina(safePage + 1)}>»</button>
      </div>

      {/* ===================== MODAL FACTURA ===================== */}
      {modalData && (
        <div className="hv-modal-back">
          <div className="hv-modal">
            <h2>Factura #{modalData.id_venta}</h2>

            <p>
              <b>Cliente:</b> {modalData.cliente}
            </p>
            <p>
              <b>Empleado:</b> {modalData.empleado}
            </p>
            <p>
              <b>Fecha:</b>{" "}
              {modalData.fecha
                ? new Date(modalData.fecha).toLocaleString()
                : ""}
            </p>

            <h3>Productos</h3>
            {Array.isArray(modalData.detalles) &&
            modalData.detalles.length > 0 ? (
              modalData.detalles.map((d) => (
                <p key={d.id_dv}>
                  {d.producto} — {d.cantidad} × ${d.precio_unit} =
                  <b> ${d.sub_total}</b>
                </p>
              ))
            ) : (
              <p>No hay productos registrados para esta venta.</p>
            )}

            <h3>Total: ${modalData.total}</h3>

            <button
              className="hv-btn-close"
              onClick={() => setModalData(null)}
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
