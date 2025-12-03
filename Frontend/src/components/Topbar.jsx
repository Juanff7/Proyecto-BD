import {FiBell, FiUser} from "react-icons/fi"
import "./../styles/topbar.css"

export default function Topbar(){
    return(
        <div className="topbar">
            <div className="topbar-title">
            Sportcity
            </div>

            <div className="topbar-right"> 
                 {/* Notificaciones */}
                <FiBell className="topbar-icon" />
                {/* Usuario */}
                <div className="user-box">
                <FiUser className="user-icon" />
               <span className="user-role">Admin</span>
                </div>
            </div>

        </div>
    );
}