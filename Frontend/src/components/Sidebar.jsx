import { useState } from "react";
import {FiHome, FiShoppingCart, FiChevronDown, FiDollarSign} from "react-icons/fi";
import { FaStore } from "react-icons/fa6";

import { Link } from "react-router-dom";




export default function Sidebar(){
   const [openCompra, setOpenCompra] = useState(false)
   const [openVenta, setOpenVenta] = useState(false)
   const [openAlmacen, setOpenAlmacen] = useState(false)


return(
    <div className="sidebar">
        <div className="sidebar-logo">
               <img src="/logoneg.jpeg" className="logo-img" alt="logo-img" />
        </div>

        <div className="sidebar-section">
          {/*Inicio(Fi home logo)*/}      
        <div className="sidebar-item">
            <FiHome className="icon" />
            inicio
            </div>
        {/*Compra(Fishoping loco de compra*/}
        <div className="sidebar-item sidebar-dropdown" onClick={() => setOpenCompra(!openCompra)}>   
            <FiShoppingCart className="icon"/> 
        Compra
          <FiChevronDown className={`chevron ${openCompra ? "rotate" : ""}`} />
        </div> 
        {openCompra && (
            <div className="sidebar-submenu">
                <Link to="/Compra/generar" className="sidebar-subitem">Registrar Compra</Link>
                <Link to="/Compra/Historial"className="sidebar-subitem">Registro</Link>
                <Link to ="Compra/Proveedor" className="sidebar-subitem">Proveedores</Link>
            </div>
        )}

        {/*Venta */}
        <div className="sidebar-item sidebar-dropdown" onClick={() => setOpenVenta(!openVenta)}>  
        <FiDollarSign className="icon"/>
        Ventas
          <FiChevronDown className={`chevron ${openVenta ? "rotate" : ""}`} />
        </div> 
        {openVenta && (
            <div className="sidebar-submenu">
                <Link to ="/Venta/generar" className="sidebar-subitem">Generar ventas</Link>
                 <Link to= "/Venta/Detalle"className="sidebar-subitem">DetallesVenta </Link>
                <Link  to="Venta/Historial"  className="sidebar-subitem">Registro de ventas </Link>
               
                <Link to="Venta/Cliente" className="sidebar-subitem">Clientes </Link>
            </div>
        )}

        <div className="sidebar-item sidebar-dropdown" onClick={() => setOpenAlmacen(!openAlmacen)}>
        <FaStore className="icon" />
        Almacen
        <FiChevronDown className={`chevron ${openAlmacen ? "rotate" : ""}`} />
        </div>
        {openAlmacen && (
            <div className="sidebar-submenu">
                <Link to="/almacen/generar"  className="sidebar-subitem">Generar Producto</Link>
                  <Link to="/historial/agregar"  className="sidebar-subitem">Cambiar Precios</Link>
                <Link  to= "/almacen/historial"className="sidebar-subitem">Historial de Precios </Link>
                <Link to="/almacen/inventario" className="sidebar-subitem">Inventario </Link>
            </div>
        )}

       

        </div>
    </div>
);

}
