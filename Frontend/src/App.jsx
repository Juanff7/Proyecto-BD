import { BrowserRouter, Routes, Route } from "react-router-dom";
import DashboardLayout from "./layout/DashboardLayout";
import Home from "./pages/Home";
import GenerarProductoPage from "./pages/almacen/GenerarProductoPage"
import GenerarCompra from "./pages/Compra/RegistroCompra"
import HistorialEntradasPage from "./pages/Compra/HistorialEntradaPage";

import ActualizarProductoPage from "./pages/almacen/HistorialPreciosPage"
import RegistrarCambioPrecio from "./pages/almacen/CambiarPrecio";

import InventarioPage from "./pages/almacen/InventarioPage"
import ProveedorPage from "./pages/Compra/ProveedorPage";

import GenerarVenta from "./pages/Venta/GenerarVentaPage"
import DetalleVentaPage from "./pages/Venta/DetalleVentaPage";
import ClientePage from "./pages/Venta/ClientepPage";
import HistorialVentasPage from "./pages/Venta/HistorialVenta";

function App() {
  return (
    <BrowserRouter>
      <Routes>
         {/* Layout principal*/}
        <Route path="/" element={<DashboardLayout/>}>
     
        <Route index  element={<Home />} />
        <Route path="Venta/Cliente" element={<ClientePage />} />
         <Route path="Venta/Detalle" element={<DetalleVentaPage />} />
         <Route path="Venta/generar" element={<GenerarVenta />} />
         <Route path="Venta/Historial" element={<HistorialVentasPage />} />


        <Route path="Compra/generar" element={<GenerarCompra />} />
        <Route path="Compra/Historial" element={<HistorialEntradasPage />} />
         <Route path="Compra/Proveedor" element={<ProveedorPage />} />
        

        <Route path="almacen/generar" element={<GenerarProductoPage />} />
         <Route path="historial/agregar" element={<RegistrarCambioPrecio />} />
        <Route path="almacen/historial" element={<ActualizarProductoPage/>} />
        <Route path="almacen/inventario" element={<InventarioPage />} />

        
       </Route>
      </Routes>
    
    </BrowserRouter>
  );
}

export default App;
