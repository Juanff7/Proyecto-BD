import { useEffect, useState, useRef } from "react";
import "../styles/home.css";

export default function Home() {
  const [showLogo, setShowLogo] = useState(true)

  useEffect(() =>{
       let timer;
        

       const resetInactivity = () => {
         setShowLogo(false) //oculta el logo cuando el usuario toca algo
         clearTimeout(timer);

         //despues de cierto tiempo inactivo, vuelve a aparecer

         timer = setTimeout(() => {
           setShowLogo(true)
         }, 2000); // 2 minutos
       };

       //detectar inactividad
       window.addEventListener("mousemove", resetInactivity)
       window.addEventListener("keydown", resetInactivity)
       window.addEventListener("click", resetInactivity)
   

       return() => {
           window.removeEventListener("mousemove", resetInactivity)
           window.removeEventListener("keydown", resetInactivity)
           window.removeEventListener("click", resetInactivity)
           clearTimeout(timer);
       };

  

  }, [])

  return (
    <div className="home-container">
      {showLogo && (
    <div className="logoHome">
      <img src="/logoneg.jpeg" className="logo-imgHome" alt="logo" />
    </div>
      )}
    </div>
  );
}
