import { useState, useEffect } from "react";
import axios from "axios";
import "../../styles/cliente.css";

const API_BASE = "http://localhost:8000/Cliente";

export default function ClientePage() {
  const [clientes, setClientes] = useState([]);
  const [form, setForm] = useState({
    nombre: "",
    direccion: "",
    telefono: "",
  });

  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [search, setSearch] = useState("");

  const cargarClientes = async () => {
    try {
      const res = await axios.get(`${API_BASE}/Obtener`);
      setClientes(res.data);
    } catch {
      console.log("Error al cargar clientes");
    }
  };

  useEffect(() => {
    cargarClientes();
  }, []);

  // Crear
  const handleCrear = async (e) => {
    e.preventDefault();
    if (!form.nombre.trim()) return alert("El nombre es obligatorio.");

    await axios.post(`${API_BASE}/Create`, form);
    cargarClientes();
    setForm({ nombre: "", direccion: "", telefono: "" });
  };

  // Eliminar
  const handleEliminar = async (id) => {
    if (!window.confirm("¿Eliminar cliente?")) return;
    await axios.delete(`${API_BASE}/delete/${id}`);
    cargarClientes();
  };

  // Editar inline
  const empezarEdicion = (cliente) => {
    setEditId(cliente.id_cliente);
    setEditForm({ ...cliente });
  };

  const guardarEdicion = async (id) => {
    await axios.put(`${API_BASE}/update/${id}`, editForm);
    setEditId(null);
    cargarClientes();
  };

  const filtered = clientes.filter((c) =>
    `${c.nombre} ${c.direccion} ${c.telefono}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="cli-container">
      <h1 className="cli-title">Gestión de Clientes</h1>

      <div className="cli-layout">

        {/* IZQUIERDA */}
        <div className="cli-form">
          <h2 className="cli-form-title">Registrar Cliente</h2>

          <form onSubmit={handleCrear}>
            <label>Nombre</label>
            <input
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />

            <label>Dirección</label>
            <input
              value={form.direccion}
              onChange={(e) => setForm({ ...form, direccion: e.target.value })}
            />

            <label>Teléfono</label>
            <input
              value={form.telefono}
              onChange={(e) => setForm({ ...form, telefono: e.target.value })}
            />

            <button className="cli-btn-primary">Registrar</button>
          </form>
        </div>

        {/* DERECHA: TABLA */}
        <div className="cli-table">
          <div className="cli-table-header">
            <input
              className="cli-search"
              placeholder="Buscar cliente..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <span className="cli-table-count">
              {filtered.length} clientes mostrados
            </span>
          </div>

          <div className="cli-table-grid cli-header">
            <span>Nombre</span>
            <span>Dirección</span>
            <span>Teléfono</span>
            <span className="cli-actions">Acciones</span>
          </div>

          {filtered.map((c) => {
            const editing = editId === c.id_cliente;

            return (
              <div className="cli-table-grid cli-row" key={c.id_cliente}>

                {/* Nombre */}
                {editing ? (
                  <input
                    value={editForm.nombre}
                    onChange={(e) =>
                      setEditForm({ ...editForm, nombre: e.target.value })
                    }
                  />
                ) : (
                  <span>{c.nombre}</span>
                )}

                {/* Dirección */}
                {editing ? (
                  <input
                    value={editForm.direccion}
                    onChange={(e) =>
                      setEditForm({ ...editForm, direccion: e.target.value })
                    }
                  />
                ) : (
                  <span>{c.direccion}</span>
                )}

                {/* Teléfono */}
                {editing ? (
                  <input
                    value={editForm.telefono}
                    onChange={(e) =>
                      setEditForm({ ...editForm, telefono: e.target.value })
                    }
                  />
                ) : (
                  <span>{c.telefono}</span>
                )}

                <div className="cli-actions">
                  {editing ? (
                    <>
                      <button
                        className="cli-btn-save"
                        onClick={() => guardarEdicion(c.id_cliente)}
                      >
                        Guardar
                      </button>
                      <button
                        className="cli-btn-cancel"
                        onClick={() => setEditId(null)}
                      >
                        Cancelar
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className="cli-btn-edit"
                        onClick={() => empezarEdicion(c)}
                      >
                        Editar
                      </button>
                      <button
                        className="cli-btn-delete"
                        onClick={() => handleEliminar(c.id_cliente)}
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
