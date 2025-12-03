import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "../styles/autoinput.css";  

export default function AutoInput({ label, endpoint, value, onChange }) {
  const [sugerencias, setSugerencias] = useState([]);
  const [show, setShow] = useState(false);
  const ref = useRef(null);

  // Cerrar menú cuando clic afuera
  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setShow(false);
      }
    };
    window.addEventListener("click", handleClick);
    return () => window.removeEventListener("click", handleClick);
  }, []);

  const handleInput = async (e) => {
    const texto = e.target.value;
    onChange(texto);

    if (!texto.trim()) {
      setSugerencias([]);
      return;
    }

    try {
      const res = await axios.get(`http://localhost:8000/${endpoint}?query=${texto}`);
      setSugerencias(res.data);
      setShow(true);
    } catch {
      setSugerencias([]);
    }
  };

  return (
    <div className="auto-wrapper" ref={ref}>
      <label>{label}</label>
      <input
        type="text"
        className="auto-input"
        value={value}
        onChange={handleInput}
        autoComplete="off"
        onFocus={() => setShow(true)}
      />

      {show && sugerencias.length > 0 && (
        <div className="auto-box">
          {sugerencias.map((s, i) => (
            <div
              key={i}
              className="auto-item"
              onClick={() => {
                onChange(s.nombre || s.tipo);
                setShow(false);
              }}
            >
              {s.nombre || s.tipo}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
