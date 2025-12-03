import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "../../styles/almacen.css";

export default function GenerarProductoPage() {

  const [form, setForm] = useState({
    nombre: "",
    descripcion: "",
    categoria: "",
    costo_venta: "",
    imagen_url: "",
  });

  const [preview, setPreview] = useState(null);

  const [categorias, setCategorias] = useState([]);
  const [loadingCategorias, setLoadingCategorias] = useState(false);

  const [loadingSubmit, setLoadingSubmit] = useState(false);
  const [loadingImage, setLoadingImage] = useState(false);

  const dropdownRef = useRef(null);

  // ---------------------------------------------------
  // Cargar categorías una sola vez
  // ---------------------------------------------------
  useEffect(() => {
    const fetchCategorias = async () => {
      setLoadingCategorias(true);
      try {
        const res = await axios.get("http://localhost:8000/categoria/all");
        setCategorias(res.data);
      } catch (err) {
        console.log(err);
        setCategorias([]);
      }
      setLoadingCategorias(false);
    };
    fetchCategorias();
  }, []);


  // ---------------------------------------------------
  // Subir imagen
  // ---------------------------------------------------
  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 3 * 1024 * 1024) {
      alert("La imagen no debe superar los 3MB");
      return;
    }

    setPreview(URL.createObjectURL(file));
    setLoadingImage(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://localhost:8000/Producto/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setForm((prev) => ({
        ...prev,
        imagen_url: res.data.url
      }));

    } catch (err) {
      console.error(err);
      alert("Error al subir imagen");
    }

    setLoadingImage(false);
  };


  // ---------------------------------------------------
  // Enviar formulario
  // ---------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (form.nombre.trim().length < 2)
      return alert("El nombre debe tener al menos 2 caracteres");

    if (!form.categoria.trim())
      return alert("Debe seleccionar una categoría");

    if (Number(form.costo_venta) <= 0)
      return alert("El precio debe ser mayor a 0");

    setLoadingSubmit(true);

    try {
      await axios.post("http://localhost:8000/Producto/create", form);

      alert("Producto registrado correctamente!");

      setForm({
        nombre: "",
        descripcion: "",
        categoria: "",
        costo_venta: "",
        imagen_url: "",
      });

      setPreview(null);

    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Error al crear el producto");
    }

    setLoadingSubmit(false);
  };


  // ---------------------------------------------------
  // RENDER
  // ---------------------------------------------------
  return (
    <div className="compra-wrapper">

      <h2 className="Title">Registrar Nuevo Producto</h2>

      <div className="compra-grid">

        {/* ------------------------------- */}
        {/*        COLUMNA IZQUIERDA       */}
        {/* ------------------------------- */}
        <div className="columna-form">

          <form onSubmit={handleSubmit}>

            {/* Nombre */}
            <label className="section-title">Información del producto</label>

            <label className="form-label">Nombre del producto</label>
            <input
              className="form-input"
              type="text"
              value={form.nombre}
              placeholder="Ingrese nombre..."
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            />

            {/* Descripción */}
            <label className="form-label">Descripción</label>
            <textarea
              className="form-textarea"
              value={form.descripcion}
              placeholder="Escriba una descripción..."
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
            />

            {/* Categoría */}
            <label className="form-label">Categoría</label>
            <select
              className="form-input"
              value={form.categoria}
              onChange={(e) => setForm({ ...form, categoria: e.target.value })}
            >
              <option value="">Seleccione una categoría</option>
              {categorias.map((c) => (
                <option key={c.id} value={c.tipo}>
                  {c.tipo}
                </option>
              ))}
            </select>

            {/* Precio */}
            <label className="form-label">Precio de venta</label>
            <input
              className="form-input"
              type="number"
              min="1"
              value={form.costo_venta}
              placeholder="0.00"
              onChange={(e) => setForm({ ...form, costo_venta: e.target.value })}
            />


            {/* Imagen */}
            <label className="section-title">Imagen del producto</label>

            <div className="file-input-wrapper">
              <input
                type="file"
                className="file-input"
                accept="image/*"
                onChange={handleImageUpload}
              />
              <span className="file-label">Seleccionar archivo</span>
            </div>

            {preview && (
              <img src={preview} className="resumen-img" />
            )}

            {/* Botón */}
            <button type="submit" className="btn-primary">
              {loadingSubmit ? "Creando..." : "Crear Producto"}
            </button>

          </form>
        </div>


        {/* ------------------------------- */}
        {/*       COLUMNA DERECHA          */}
        {/*       (Vista previa total)     */}
        {/* ------------------------------- */}
        <div className="columna-resumen">

          <h3 className="resumen-title">Vista previa</h3>

          {preview ? (
            <img src={preview} className="resumen-img" />
          ) : (
            <p className="resumen-card">No hay imagen seleccionada.</p>
          )}

          <hr />

          <div className="resumen-card">
            <p><strong>Nombre:</strong> {form.nombre || "—"}</p>
            <p><strong>Descripción:</strong> {form.descripcion || "—"}</p>
            <p><strong>Categoría:</strong> {form.categoria || "—"}</p>
            <p><strong>Precio:</strong> {form.costo_venta ? `$${form.costo_venta}` : "—"}</p>
          </div>

        </div>

      </div>
    </div>
  );
}
