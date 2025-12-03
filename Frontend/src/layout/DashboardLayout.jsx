import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import "../styles/sidebar.css";
import "../styles/Topbar.css"
import "../styles/dashboard.css";  


export default function DashboardLayout({children}){
    return(
        <div className="dashboard-container">
            <Sidebar />
       
         <div className="dashboard-main">
              <Topbar/ >
              
            <div className="dashboard-content">
            <Outlet />
        </div>
    </div>
</div>

    )
    
}