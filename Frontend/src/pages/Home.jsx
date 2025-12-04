import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { Link } from "react-router-dom";
import { FiShoppingBag, FiTag, FiPackage } from "react-icons/fi";


import "../styles/home.css";

const API = "http://localhost:8000/Dashboard/";

export default function HomeDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get(API).then((res) => setStats(res.data));
  }, []);

  if (!stats) return <h2 className="loading">Cargando Dashboard...</h2>;

  return (
    <div className="home-wrapper">

      {/* ---- TOP CARDS ---- */}
    <div className="cards-grid">
  <Card
    title="Ventas Mes Actual"
    value={`$${(stats.ventas_mes_actual ?? 0).toFixed(2)}`}
  />

  <Card
    title="Producto Más Vendido"
    value={stats.producto_mas_vendido?.nombre ?? "Sin datos"}
  />

  <Card
    title="Más Comprado a Proveedor"
    value={stats.producto_mas_comprado?.nombre ?? "Sin datos"}
  />

  <Card
    title="Movimientos de Precios"
    value={stats.movimientos_precios ?? 0}
  />

  <Card
    title="Subidas / Bajadas"
    value={`${stats.subidas ?? 0} / ${stats.bajadas ?? 0}`}
  />
</div>


      {/* ---- GRÁFICAS ---- */}
      <div className="charts-grid">

        <ChartBlock title="Ventas por Mes">
          <ResponsiveContainer width="100%" height={180}>
           <BarChart data={stats.ventas_por_mes ?? []}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis dataKey="mes" tick={{ fill: "#c9ced8" }} />
              <YAxis tick={{ fill: "#c9ced8" }} />
              <Tooltip contentStyle={{ background: "#1d242f", borderRadius: 10 }} />
              <Bar dataKey="total" fill="#4da3ff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartBlock>

        <ChartBlock title="Productos Más Vendidos">
          <ResponsiveContainer width="100%" height={180}>
           <BarChart data={stats.top_vendidos ?? []}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis dataKey="nombre" tick={{ fill: "#c9ced8" }} />
              <YAxis tick={{ fill: "#c9ced8" }} />
              <Tooltip contentStyle={{ background: "#1d242f", borderRadius: 10 }} />
              <Bar dataKey="cantidad" fill="#a68eff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartBlock>

        <ChartBlock title="Productos Más Comprados">
          <ResponsiveContainer width="100%" height={180}>
           <BarChart data={stats.top_comprados ?? []}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis dataKey="nombre" tick={{ fill: "#c9ced8" }} />
              <YAxis tick={{ fill: "#c9ced8" }} />
              <Tooltip contentStyle={{ background: "#1d242f", borderRadius: 10 }} />
              <Bar dataKey="cantidad" fill="#4df2b0" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartBlock>

      </div>
     {/* ---- ACCESOS RÁPIDOS ---- */}
<div className="quick-actions">
  <QuickButton 
    title="Registrar Compra" 
    link="/Compra/generar" 
    Icon={FiShoppingBag}
  />

  <QuickButton 
    title="Generar Venta" 
    link="/Venta/generar" 
    Icon={FiTag}
  />

  <QuickButton 
    title="Crear Producto" 
    link="/almacen/generar"
    Icon={FiPackage}
  />
</div>



    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="apple-card">
      <h4>{title}</h4>
      <p>{value}</p>
    </div>
  );
}

function ChartBlock({ title, children }) {
  return (
    <div className="apple-chart">
      <h3>{title}</h3>
      {children}
    </div>
  );
}
function QuickButton({ title, link, Icon }) {
  return (
    <Link to={link} className="quick-btn">
      <Icon className="quick-icon" />
      <span>{title}</span>
    </Link>
  );
}

