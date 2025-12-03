import { useState, useEffect, useMemo } from "react";
import axios from "axios";
import "../../styles/HistorialEntradas.css";
import * as XLSX from "xlsx";

const API = "http://localhost:8000/Entrada";

export default function HistorialEntradasPage() {
  const [entradas, setEntradas] = useState([]);
  const [search, setSearch] = useState("");

  const [fecha, setFecha] = useState("");
  const [inicio, setInicio] = useState("");
  const [fin, setFin] = useState("");

  const [modalData, setModalData] = useState(null);

  const [page, setPage] = useState(1);
  const pageSize = 10;

  // =======================
  // CARGAR HISTORIAL COMPLETO
  // =======================
  const cargarHistorial = async () => {
    const res = await axios.get(`${API}/obtener`);
    setEntradas(res.data);
    setPage(1);
  };

  useEffect(() => {
    cargarHistorial();
  }, []);

  // =======================
  // FILTRAR POR FECHA ÚNICA
  // =======================
  const filtrarFecha = async () => {
    if (!fecha) return cargarHistorial();
    const res = await axios.get(`${API}/buscar_fecha/${fecha}`);
    setEntradas(res.data);
    setPage(1);
  };

  // =======================
  // FILTRAR POR RANGO
  // =======================
  const filtrarRango = async () => {
    if (!inicio || !fin) return alert("Selecciona ambas fechas.");
    const res = await axios.get(`${API}/rango`, {
      params: { inicio, fin },
    });
    setEntradas(res.data);
    setPage(1);
  };

  // =======================
  // BUSQUEDA GLOBAL
  // =======================
  const filtrados = useMemo(
    () =>
      entradas.filter((e) =>
        `${e.producto?.nombre || ""} ${e.proveedor?.nombre || ""} ${
          e.empleado?.nombre || ""
        } ${e.detalle || ""}`
          .toLowerCase()
          .includes(search.toLowerCase())
      ),
    [entradas, search]
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
  // HISTOGRAMA – TOP PROVEEDORES
  // =======================
  const statsProveedores = useMemo(() => {
    const mapa = new Map();
    for (const e of filtrados) {
      const n = e.proveedor?.nombre || "Desconocido";
      const subtotal = (e.cantidad || 0) * (e.precio_unit || 0);
      mapa.set(n, (mapa.get(n) || 0) + subtotal);
    }
    return [...mapa.entries()]
      .map(([proveedor, total]) => ({ proveedor, total }))
      .sort((a, b) => b.total - a.total);
  }, [filtrados]);

  const maxProveedorTotal = statsProveedores[0]?.total || 1;

  // =======================
  // EXPORTAR EXCEL
  // =======================
 const exportarExcel = () => {
  if (!filtrados.length) return alert("No hay datos para exportar.");

  // Preparar datos para Excel
  const data = filtrados.map((e) => ({
    ID: e.id_dp,
    Producto: e.producto?.nombre || "",
    Proveedor: e.proveedor?.nombre || "",
    Empleado: e.empleado?.nombre || "",
    Cantidad: e.cantidad,
    PrecioUnit: e.precio_unit,
    Subtotal: (e.cantidad || 0) * (e.precio_unit || 0),
    Fecha: new Date(e.fecha_ingreso).toLocaleString(),
    Detalle: e.detalle || "",
  }));

  // Crear hoja
  const worksheet = XLSX.utils.json_to_sheet(data);

  // Ajustar ancho de columnas automáticamente
  const colWidths = Object.keys(data[0]).map((key) => ({
    wch: Math.max(
      key.length,
      ...data.map((row) => String(row[key] || "").length)
    ) + 2,
  }));

  worksheet["!cols"] = colWidths;

  // Crear libro
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Entradas");

  // Descargar archivo
  XLSX.writeFile(workbook, "Historial_Entradas.xlsx");
};

  // =======================
  // EXPORTAR PDF GENERAL
  // =======================
  const exportarPDF = async () => {
    if (!filtrados.length) return alert("No hay datos para el PDF.");

    const payload = {
      filtros: {
        search,
        fecha,
        inicio,
        fin,
      },
      entradas: filtrados.map((e) => ({
        id_dp: e.id_dp,
        producto: e.producto?.nombre || "",
        proveedor: e.proveedor?.nombre || "",
        empleado: e.empleado?.nombre || "",
        cantidad: e.cantidad,
        precio_unit: e.precio_unit,
        fecha_ingreso: e.fecha_ingreso,
        detalle: e.detalle,
      })),
    };

    const res = await axios.post(`${API}/reporte/general`, payload, {
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "reporte_entradas.pdf");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  // =======================
  // ELIMINAR
  // =======================
  const eliminarEntrada = async (id) => {
    if (!confirm("¿Eliminar esta entrada? Se revertirá el stock.")) return;
    await axios.delete(`${API}/eliminar/${id}`);
    cargarHistorial();
  };

  // =======================
  // TOTALES
  // =======================
  const totalMonto = filtrados.reduce(
    (acc, e) => acc + e.cantidad * e.precio_unit,
    0
  );

  return (
    <div className="he-container">
      <h1 className="he-title">Historial de Entradas</h1>

      {/* ===================== FILTROS ===================== */}
      <div className="he-filtros">
        <input
          className="he-input he-input-wide"
          placeholder="Buscar producto, proveedor, empleado..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="he-filter-group">
          <label>Fecha</label>
          <div className="he-filter-row">
            <input
              type="date"
              className="he-input"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
            />
            <button className="he-btn" onClick={filtrarFecha}>
              Buscar
            </button>
          </div>
        </div>

        <div className="he-filter-group">
          <label>Rango</label>
          <div className="he-filter-row">
            <input
              type="date"
              className="he-input"
              value={inicio}
              onChange={(e) => setInicio(e.target.value)}
            />
            <input
              type="date"
              className="he-input"
              value={fin}
              onChange={(e) => setFin(e.target.value)}
            />
            <button className="he-btn" onClick={filtrarRango}>
              Aplicar
            </button>
          </div>
        </div>

        <div className="he-filter-group">
          <label>Exportar</label>
          <div className="he-filter-row">
            <button className="he-btn-excel" onClick={exportarExcel}>
              Excel
            </button>
            <button className="he-btn-pdf" onClick={exportarPDF}>
              PDF
            </button>
            <button className="he-btn-secondary" onClick={cargarHistorial}>
              Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* ===================== RESUMEN ===================== */}
      <div className="he-summary">
        <div className="he-card">
          <span className="he-card-label">Total de entradas</span>
          <span className="he-card-value">{filtrados.length}</span>
        </div>

        <div className="he-card">
          <span className="he-card-label">Monto total</span>
          <span className="he-card-value">
            ${totalMonto.toFixed(2)}
          </span>
        </div>

        {statsProveedores[0] && (
          <div className="he-card">
            <span className="he-card-label">Proveedor top</span>
            <span className="he-card-value">
              {statsProveedores[0].proveedor}
            </span>
          </div>
        )}
      </div>

      {/* ===================== HISTOGRAMA ===================== */}
      <div className="he-stats">
        <h2 className="he-subtitle">Proveedores por monto comprado</h2>
        {statsProveedores.length === 0 ? (
          <p>No hay datos.</p>
        ) : (
          <div className="he-chart">
            {statsProveedores.map((p) => (
              <div className="he-bar" key={p.proveedor}>
                <span className="he-bar-label">
                  {p.proveedor} — ${p.total.toFixed(2)}
                </span>
                <div className="he-bar-track">
                  <div
                    className="he-bar-fill"
                    style={{
                      width: `${(p.total / maxProveedorTotal) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ===================== TABLA ===================== */}
      <div className="he-table">
        <div className="he-row he-header">
          <span>ID</span>
          <span>Producto</span>
          <span>Proveedor</span>
          <span>Empleado</span>
          <span>Cantidad</span>
          <span>Precio</span>
          <span>Fecha</span>
          <span>Acciones</span>
        </div>

        {dataPage.map((e) => (
          <div className="he-row" key={e.id_dp}>
            <span>{e.id_dp}</span>
            <span>{e.producto?.nombre}</span>
            <span>{e.proveedor?.nombre}</span>
            <span>{e.empleado?.nombre}</span>
            <span>{e.cantidad}</span>
            <span>${e.precio_unit}</span>
            <span>{new Date(e.fecha_ingreso).toLocaleString()}</span>

            <div className="he-actions">
              <button className="he-btn-detalle" onClick={() => setModalData(e)}>
                Ver
              </button>

              <button
                className="he-btn-delete"
                onClick={() => eliminarEntrada(e.id_dp)}
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}

        {dataPage.length === 0 && (
          <div className="he-row he-empty-row">
            <span>No hay registros.</span>
          </div>
        )}
      </div>

      {/* ===================== PAGINACIÓN ===================== */}
      <div className="he-pagination">
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

      {/* ===================== MODAL ===================== */}
      {modalData && (
        <div className="he-modal-back">
          <div className="he-modal">
            <h2>Detalle #{modalData.id_dp}</h2>

            <p><b>Producto:</b> {modalData.producto?.nombre}</p>
            <p><b>Proveedor:</b> {modalData.proveedor?.nombre}</p>
            <p><b>Empleado:</b> {modalData.empleado?.nombre}</p>
            <p><b>Cantidad:</b> {modalData.cantidad}</p>
            <p><b>Precio Unit:</b> ${modalData.precio_unit}</p>
            <p><b>Subtotal:</b> ${(modalData.cantidad * modalData.precio_unit).toFixed(2)}</p>
            <p><b>Fecha:</b> {new Date(modalData.fecha_ingreso).toLocaleString()}</p>
            {modalData.detalle && <p><b>Detalle:</b> {modalData.detalle}</p>}

            <button className="he-btn-close" onClick={() => setModalData(null)}>
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
