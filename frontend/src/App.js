import { BrowserRouter , Route, Routes } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

import Header from './components/Header'
import Home from './components/Home'
import Actors from './components/actors';
import Movies from './components/movies';
import Login from './components/login';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header/>
          <Routes>
            <Route path='/' element={<Home/>}></Route>
            <Route path='/actors' element={<Actors/>}></Route>
            <Route path='/movies' element={<Movies/>}></Route>
            <Route path='/actors/:id'></Route>
            <Route path='/movies/:id'></Route>
          </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
