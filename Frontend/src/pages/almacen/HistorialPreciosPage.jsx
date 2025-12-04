import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "../../styles/HistorialPrecios.css";

const API = "http://localhost:8000/Historial"; // ajusta si tu prefix es otro

export default function HistorialPreciosPage() {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(false);

  // Filtros
  const [productId, setProductId] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  // Ordenamiento
  const [sortKey, setSortKey] = useState("fecha_de_cambio");
  const [sortDir, setSortDir] = useState("desc");

  // Paginación
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const cargarHistorial = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API}/`);
      setHistorial(res.data || []);
    } catch (err) {
      console.error("Error cargando historial de precios", err);
      setHistorial([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarHistorial();
  }, []);

  // Helpers
  const formatFecha = (fechaStr) => {
    if (!fechaStr) return "-";
    const d = new Date(fechaStr);
    if (Number.isNaN(d.getTime())) return fechaStr;
    return d.toLocaleString();
  };

  const formatMoneda = (v) => {
    if (v === null || v === undefined) return "-";
    return `$${Number(v).toFixed(2)}`;
  };

  // Aplicar filtros + ordenamiento
  const filtradosYOrdenados = useMemo(() => {
    let data = [...historial];

   // Filtrar por ID O nombre del producto
if (productId.trim()) {
  const term = productId.trim().toLowerCase();

  data = data.filter((h) => {
    const idMatch = String(h.id_producto).includes(term);
    const nameMatch = h.producto?.nombre
      ?.toLowerCase()
      .includes(term);

    return idMatch || nameMatch;
  });
}


    // Filtrar por rango de fechas
    if (dateFrom) {
      const dFrom = new Date(dateFrom);
      data = data.filter((h) => new Date(h.fecha_de_cambio) >= dFrom);
    }
    if (dateTo) {
      // incluir todo el día "hasta"
      const dTo = new Date(dateTo);
      dTo.setHours(23, 59, 59, 999);
      data = data.filter((h) => new Date(h.fecha_de_cambio) <= dTo);
    }

    // Ordenar
    data.sort((a, b) => {
      let vA = a[sortKey];
      let vB = b[sortKey];

      if (sortKey === "fecha_de_cambio") {
        vA = new Date(vA).getTime();
        vB = new Date(vB).getTime();
      }

      if (vA < vB) return sortDir === "asc" ? -1 : 1;
      if (vA > vB) return sortDir === "asc" ? 1 : -1;
      return 0;
    });

    return data;
  }, [historial, productId, dateFrom, dateTo, sortKey, sortDir]);

  // Paginación
  const total = filtradosYOrdenados.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const pageSafe = Math.min(page, totalPages);
  const startIdx = (pageSafe - 1) * pageSize;
  const currentPageData = filtradosYOrdenados.slice(
    startIdx,
    startIdx + pageSize
  );

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
  };

  const limpiarFiltros = () => {
    setProductId("");
    setDateFrom("");
    setDateTo("");
    setPage(1);
  };

  // Resumen rápido (subidas / bajadas)
  const stats = useMemo(() => {
    let subidas = 0;
    let bajadas = 0;
    filtradosYOrdenados.forEach((h) => {
      if (h.precio_anterior == null || h.precio_nuevo == null) return;
      const diff = Number(h.precio_nuevo) - Number(h.precio_anterior);
      if (diff > 0) subidas++;
      else if (diff < 0) bajadas++;
    });
    return { subidas, bajadas, total: filtradosYOrdenados.length };
  }, [filtradosYOrdenados]);

  return (
    <div className="hist-container">
      <h1 className="hist-title">Historial de Precios</h1>

      {/* ================== FILTROS + RESUMEN ================== */}
      <div className="hist-top">
        <div className="hist-filters">
          <div className="hist-filter-group">
            <label>Producto</label>
            <input
              className="hist-input"
              type="text"
              placeholder="Dudley o 5"
              value={productId}
              onChange={(e) => {
                setProductId(e.target.value);
                setPage(1);
              }}
            />
          </div>

          <div className="hist-filter-group">
            <label>Desde</label>
            <input
              className="hist-input"
              type="date"
              value={dateFrom}
              onChange={(e) => {
                setDateFrom(e.target.value);
                setPage(1);
              }}
            />
          </div>

          <div className="hist-filter-group">
            <label>Hasta</label>
            <input
              className="hist-input"
              type="date"
              value={dateTo}
              onChange={(e) => {
                setDateTo(e.target.value);
                setPage(1);
              }}
            />
          </div>

          <div className="hist-filter-buttons">
            <button className="hist-btn-secondary" onClick={limpiarFiltros}>
              Limpiar filtros
            </button>
            <button className="hist-btn-refresh" onClick={cargarHistorial}>
              Recargar
            </button>
          </div>
        </div>

        <div className="hist-summary">
          <div className="hist-summary-card">
            <span className="hist-summary-label">Cambios totales</span>
            <span className="hist-summary-value">{stats.total}</span>
          </div>
          <div className="hist-summary-card hist-summary-up">
            <span className="hist-summary-label">Subidas de precio</span>
            <span className="hist-summary-value">{stats.subidas}</span>
          </div>
          <div className="hist-summary-card hist-summary-down">
            <span className="hist-summary-label">Bajadas de precio</span>
            <span className="hist-summary-value">{stats.bajadas}</span>
          </div>
        </div>
      </div>

      {/* ================== TABLA ================== */}
      <div className="hist-table-wrapper">
        <div className="hist-row hist-header-row">
          <span
            className="hist-col-id hist-header-click"
            onClick={() => handleSort("id")}
          >
            ID
            {sortKey === "id" && (
              <span className="hist-sort-indicator">
                {sortDir === "asc" ? "▲" : "▼"}
              </span>
            )}
          </span>
          <span
            className="hist-col-product hist-header-click"
            onClick={() => handleSort("id_producto")}
          >
            Producto
            {sortKey === "id_producto" && (
              <span className="hist-sort-indicator">
                {sortDir === "asc" ? "▲" : "▼"}
              </span>
            )}
          </span>
          <span
            className="hist-col-price hist-header-click"
            onClick={() => handleSort("precio_anterior")}
          >
            Precio anterior
            {sortKey === "precio_anterior" && (
              <span className="hist-sort-indicator">
                {sortDir === "asc" ? "▲" : "▼"}
              </span>
            )}
          </span>
          <span
            className="hist-col-price hist-header-click"
            onClick={() => handleSort("precio_nuevo")}
          >
            Precio nuevo
            {sortKey === "precio_nuevo" && (
              <span className="hist-sort-indicator">
                {sortDir === "asc" ? "▲" : "▼"}
              </span>
            )}
          </span>
          <span className="hist-col-change">Variación</span>
          <span
            className="hist-col-date hist-header-click"
            onClick={() => handleSort("fecha_de_cambio")}
          >
            Fecha de cambio
            {sortKey === "fecha_de_cambio" && (
              <span className="hist-sort-indicator">
                {sortDir === "asc" ? "▲" : "▼"}
              </span>
            )}
          </span>
        </div>

        {loading && (
          <div className="hist-row hist-row-empty">
            <span>Cargando historial...</span>
          </div>
        )}

        {!loading && currentPageData.length === 0 && (
          <div className="hist-row hist-row-empty">
            <span>No hay cambios de precio con los filtros actuales.</span>
          </div>
        )}

        {!loading &&
          currentPageData.map((h) => {
            const anterior = h.precio_anterior;
            const nuevo = h.precio_nuevo;
            let diff = null;
            let diffPct = null;

            if (anterior != null && nuevo != null && Number(anterior) !== 0) {
              diff = Number(nuevo) - Number(anterior);
              diffPct = (diff / Number(anterior)) * 100;
            }

            const esSubida = diff != null && diff > 0;
            const esBajada = diff != null && diff < 0;

            return (
              <div className="hist-row" key={h.id}>
                <span className="hist-col-id">
                  <span className="hist-id-pill">{h.id_producto}</span>
                </span>

              <span className="hist-col-product">
  <span className="hist-product-name">
    {h.producto?.nombre ?? "Producto eliminado"}
  </span>
</span>


                <span className="hist-col-price">
                  {formatMoneda(anterior)}
                </span>
                <span className="hist-col-price">
                  {formatMoneda(nuevo)}
                </span>

                <span className="hist-col-change">
                  {diff == null ? (
                    <span className="hist-chip neutral">—</span>
                  ) : (
                    <span
                      className={
                        "hist-chip " +
                        (esSubida ? "up" : esBajada ? "down" : "neutral")
                      }
                    >
                      {esSubida && "▲ "}
                      {esBajada && "▼ "}
                      {formatMoneda(Math.abs(diff))}{" "}
                      {diffPct != null && (
                        <span className="hist-chip-pct">
                          ({diffPct.toFixed(1)}%)
                        </span>
                      )}
                    </span>
                  )}
                </span>

                <span className="hist-col-date">
                  {formatFecha(h.fecha_de_cambio)}
                </span>
              </div>
            );
          })}
      </div>

      {/* ================== PAGINACIÓN ================== */}
      {total > 0 && (
        <div className="hist-footer">
          <span className="hist-footer-count">
            Mostrando{" "}
            <strong>
              {startIdx + 1}-{Math.min(startIdx + pageSize, total)}
            </strong>{" "}
            de <strong>{total}</strong> cambios
          </span>

          <div className="hist-pagination">
            <button
              className="hist-page-btn"
              disabled={pageSafe === 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Anterior
            </button>

            {Array.from({ length: totalPages }).map((_, idx) => {
              const num = idx + 1;
              return (
                <button
                  key={num}
                  className={
                    "hist-page-btn " +
                    (num === pageSafe ? "hist-page-btn-active" : "")
                  }
                  onClick={() => setPage(num)}
                >
                  {num}
                </button>
              );
            })}

            <button
              className="hist-page-btn"
              disabled={pageSafe === totalPages}
              onClick={() =>
                setPage((p) => Math.min(totalPages, p + 1))
              }
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
