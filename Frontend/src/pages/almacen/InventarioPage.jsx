import { useEffect, useState } from "react";
import axios from "axios";
import "../../styles/InventarioPage.css";

const API = "http://localhost:8000/Producto";

export default function InventarioPage() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);

  const [search, setSearch] = useState("");
  const [filtroCategoria, setFiltroCategoria] = useState("");

  // =========================
  // MODAL DE EDICIÓN
  // =========================
  const [modalOpen, setModalOpen] = useState(false);
  const [editForm, setEditForm] = useState({});
  const [productoEditando, setProductoEditando] = useState(null);

  // =========================
  // CARGAR PRODUCTOS
  // =========================
  const cargarProductos = async () => {
    try {
      const res = await axios.get(`${API}/`);
      setProductos(res.data);
    } catch (err) {
      console.log("Error cargando productos", err);
    }
  };

  // =========================
  // CARGAR CATEGORÍAS
  // =========================
  const cargarCategorias = async () => {
    try {
      const res = await axios.get("http://localhost:8000/categoria/all");
      setCategorias(res.data);
    } catch {}
  };

  useEffect(() => {
    cargarProductos();
    cargarCategorias();
  }, []);

  // =========================
  // FILTROS
  // =========================
  const filtrados = productos.filter((p) => {
    const coincideNombre = p.nombre.toLowerCase().includes(search.toLowerCase());
    const coincideCategoria =
      !filtroCategoria || p.categoria?.tipo === filtroCategoria;

    return coincideNombre && coincideCategoria;
  });

  // --------------------------------------------------
  //   ABRIR MODAL DE EDICIÓN
  // --------------------------------------------------
  const abrirModal = (p) => {
    setProductoEditando(p);
    setEditForm({
      nombre: p.nombre,
      descripcion: p.descripcion || "",
      categoria: p.categoria?.tipo || "",
      costo_venta: p.costo_venta,
      imagen_url: p.imagen_url,
    });
    setModalOpen(true);
  };

  // --------------------------------------------------
  //   GUARDAR EDICIÓN (POR ID)
  // --------------------------------------------------
const guardarCambios = async () => {
  try {
    await axios.put(`${API}/update/id/${productoEditando.id_producto}`, {
      nombre: editForm.nombre,
      descripcion: editForm.descripcion,
      categoria: editForm.categoria,
      costo_venta: Number(editForm.costo_venta),
      imagen_url: editForm.imagen_url,   // ✅ solo usamos lo que ya está en el form
    });

    alert("Producto actualizado correctamente");
    setModalOpen(false);
    cargarProductos();
  } catch (err) {
    console.log(err.response?.data || err);
    alert(err.response?.data?.detail || "Error al actualizar producto");
  }
};


  // --------------------------------------------------
  // ELIMINAR PRODUCTO
  // --------------------------------------------------
  const eliminarProducto = async (id) => {
    if (!confirm("¿Eliminar producto?")) return;

    try {
      await axios.delete(`${API}/delete/${id}`);
      cargarProductos();
    } catch {
      alert("No se pudo eliminar");
    }
  };

  // --------------------------------------------
// MANEJAR IMAGEN — PREVIEW + SUBIR AL BACKEND
// --------------------------------------------
const manejarImagen = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // Crear preview local
  const previewURL = URL.createObjectURL(file);
  setEditForm((prev) => ({ ...prev, preview: previewURL }));

  // Subir al backend
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post(`${API}/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    // Guardar la URL del backend
    setEditForm((prev) => ({
      ...prev,
      imagen_url: res.data.url,
    }));
  } catch (error) {
    console.log("Error al subir imagen", error);
    alert("No se pudo subir la imagen");
  }
};

  return (
    <div className="prod-container">
      <h1 className="prod-title">Inventario de Productos</h1>

      {/* ======================= BUSCADOR Y FILTRO ======================= */}
      <div className="prod-header">
        <input
          className="prod-search"
          placeholder="Buscar producto..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          className="prod-filter"
          value={filtroCategoria}
          onChange={(e) => setFiltroCategoria(e.target.value)}
        >
          <option value="">Todas las categorías</option>
          {categorias.map((c) => (
            <option key={c.id_categoria} value={c.tipo}>
              {c.tipo}
            </option>
          ))}
        </select>
      </div>

      {/* ======================= TABLA ======================= */}
      <div className="prod-table">
       <div className="prod-row prod-header-row">
  <span>ID</span>
  <span>Imagen</span>
  <span>Nombre</span>
  <span>Categoría</span>
  <span>Precio</span>
  <span>Stock</span>
  <span className="prod-actions-col">Acciones</span>
</div>


        {filtrados.map((p) => (
 <div className="prod-row" key={p.id_producto}>
  
  {/* ID */}
  <span className="prod-id">{p.id_producto}</span>

  {/* Imagen */}
  <div className="prod-img-box">
    <img src={p.imagen_url || "/no-image.png"} className="prod-img" alt="img" />
  </div>

  <span>{p.nombre}</span>
  <span>{p.categoria?.tipo || "Sin categoría"}</span>
  <span>${p.costo_venta}</span>
  <span>{p.cantidad}</span>

  <div className="prod-actions">
    <button
      className="prod-btn-edit"
      onClick={() => abrirModal(p)}
    >
      Editar
    </button>
    <button
      className="prod-btn-delete"
      onClick={() => eliminarProducto(p.id_producto)}
    >
      Eliminar
    </button>
  </div>
</div>

        ))}
      </div>

      <p className="prod-count">{filtrados.length} productos mostrados</p>

      {/* ======================= MODAL DE EDICIÓN ======================= */}
      {modalOpen && (
        <div className="prod-modal-backdrop">
          <div className="prod-modal">
            <h2>Editar Producto</h2>

            <label>Nombre</label>
            <input
              value={editForm.nombre}
              onChange={(e) =>
                setEditForm({ ...editForm, nombre: e.target.value })
              }
            />

            <label>Descripción</label>
            <input
              value={editForm.descripcion}
              onChange={(e) =>
                setEditForm({ ...editForm, descripcion: e.target.value })
              }
            />

            <label>Categoría</label>
            <select
              value={editForm.categoria}
              onChange={(e) =>
                setEditForm({ ...editForm, categoria: e.target.value })
              }
            >
              <option value="">Sin categoría</option>
              {categorias.map((c) => (
                <option key={c.id_categoria} value={c.tipo}>
                  {c.tipo}
                </option>
              ))}
            </select>

            <label>Precio</label>
            <input
              type="number"
              value={editForm.costo_venta}
              onChange={(e) =>
                setEditForm({ ...editForm, costo_venta: e.target.value })
              }
            />

        <label>Imagen actual</label>
<div className="prod-edit-img-box">
  <img
    src={editForm.preview || editForm.imagen_url || "/no-image.png"}
    alt="preview"
  />
</div>

<label>Subir nueva imagen</label>
<input
  type="file"
  accept="image/*"
  onChange={(e) => manejarImagen(e)}
  className="prod-file-input"
/>


            <div className="modal-actions">
              <button className="btn-save" onClick={guardarCambios}>
                Guardar
              </button>
              <button className="btn-cancel" onClick={() => setModalOpen(false)}>
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
