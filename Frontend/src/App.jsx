import {BrowserRouter, Routes, Route} from 'react-router-dom'
import HomePage from './pages/homepages'
import TaskForm from './pages/TaskForm'
import Entrada from './pages/Entrada'
function App(){
  return (
    <BrowserRouter>
    <Routes>
      <Route path='/' element={<HomePage/>}/>
      <Route path='/new' element={<TaskForm/>}/>
      <Route path='/entrada'element={<Entrada/>} ></Route>
    </Routes>
    
    </BrowserRouter>
  )
}

export default App