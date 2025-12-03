import { useEffect, useState } from "react";
import axios from "axios";
import "../../styles/proveedor.css";

const API_BASE = "http://localhost:8000/Proveedor";

export default function ProveedorPage() {
  const [proveedores, setProveedores] = useState([]);
  const [loading, setLoading] = useState(false);

  // Formulario
  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    usuario_ebay: "",
    pais: "",
    tipo: "",
  });

  // Edición
  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({});

  const [search, setSearch] = useState("");

  const cargarProveedores = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/Obtener`);
      setProveedores(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarProveedores();
  }, []);

  // Crear
  const handleCrear = async (e) => {
    e.preventDefault();
    if (!form.nombre.trim()) return alert("El nombre es obligatorio.");

    await axios.post(`${API_BASE}/create`, form);
    cargarProveedores();
    setForm({
      nombre: "",
      apellido: "",
      usuario_ebay: "",
      pais: "",
      tipo: "",
    });
  };

  // Eliminar
  const handleEliminar = async (id) => {
    if (!window.confirm("¿Eliminar proveedor?")) return;
    await axios.delete(`${API_BASE}/delete/${id}`);
    cargarProveedores();
  };

  // Edición inline
  const empezarEdicion = (prov) => {
    setEditId(prov.id_proveedor);
    setEditForm({ ...prov });
  };

  const guardarEdicion = async (id) => {
    await axios.put(`${API_BASE}/update/${id}`, editForm);
    setEditId(null);
    cargarProveedores();
  };

  const filtered = proveedores.filter((p) =>
    `${p.nombre} ${p.apellido} ${p.pais} ${p.tipo} ${p.usuario_ebay}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="prov-container">
      <h1 className="prov-title">Gestión de Proveedores</h1>

      <div className="prov-layout">

        {/* IZQUIERDA */}
        <div className="prov-form">
          <h2 className="prov-form-title">Registrar Proveedor</h2>

          <form onSubmit={handleCrear}>
            <label>Nombre</label>
            <input
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />

            <label>Apellido</label>
            <input
              value={form.apellido}
              onChange={(e) => setForm({ ...form, apellido: e.target.value })}
            />

            <label>Usuario eBay</label>
            <input
              value={form.usuario_ebay}
              onChange={(e) =>
                setForm({ ...form, usuario_ebay: e.target.value })
              }
            />

            <label>País</label>
            <input
              value={form.pais}
              onChange={(e) => setForm({ ...form, pais: e.target.value })}
            />

            <label>Tipo</label>
            <input
              value={form.tipo}
              onChange={(e) => setForm({ ...form, tipo: e.target.value })}
            />

            <button className="prov-btn-primary">Registrar</button>
          </form>
        </div>

        {/* DERECHA: TABLA */}
        <div className="prov-table">
          <div className="prov-table-header">
            <input
              className="prov-search"
              placeholder="Buscar proveedor..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <span className="prov-table-count">
              {filtered.length} proveedores mostrados
            </span>
          </div>

          <div className="prov-table-grid prov-header">
            <span>Nombre</span>
            <span>País</span>
            <span>Tipo</span>
            <span>eBay</span>
            <span className="prov-actions">Acciones</span>
          </div>

          {filtered.map((p) => {
            const editing = editId === p.id_proveedor;

            return (
              <div className="prov-table-grid prov-row" key={p.id_proveedor}>

                {/* Nombre */}
                {editing ? (
                  <input
                    value={editForm.nombre}
                    onChange={(e) =>
                      setEditForm({ ...editForm, nombre: e.target.value })
                    }
                  />
                ) : (
                  <span>{p.nombre + " " + p.apellido}</span>
                )}

                {/* País */}
                {editing ? (
                  <input
                    value={editForm.pais}
                    onChange={(e) =>
                      setEditForm({ ...editForm, pais: e.target.value })
                    }
                  />
                ) : (
                  <span>{p.pais}</span>
                )}

                {/* Tipo */}
                {editing ? (
                  <input
                    value={editForm.tipo}
                    onChange={(e) =>
                      setEditForm({ ...editForm, tipo: e.target.value })
                    }
                  />
                ) : (
                  <span>{p.tipo}</span>
                )}

                {/* eBay */}
                {editing ? (
                  <input
                    value={editForm.usuario_ebay}
                    onChange={(e) =>
                      setEditForm({ ...editForm, usuario_ebay: e.target.value })
                    }
                  />
                ) : (
                  <span>{p.usuario_ebay}</span>
                )}

                <div className="prov-actions">
                  {editing ? (
                    <>
                      <button
                        className="prov-btn-save"
                        onClick={() => guardarEdicion(p.id_proveedor)}
                      >
                        Guardar
                      </button>
                      <button
                        className="prov-btn-cancel"
                        onClick={() => setEditId(null)}
                      >
                        Cancelar
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className="prov-btn-edit"
                        onClick={() => empezarEdicion(p)}
                      >
                        Editar
                      </button>
                      <button
                        className="prov-btn-delete"
                        onClick={() => handleEliminar(p.id_proveedor)}
                      >
                        Eliminar
                      </button>
                    </>
                  )}
                </div>

              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
