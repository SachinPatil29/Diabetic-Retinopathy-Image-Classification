import React from 'react';
import { BrowserRouter,Route,Routes } from 'react-router-dom';
import './App.css';
import Login from './Users/Login/Login';
import Home from './Users/Home/Home';
import Navbar from './Users/NavBar/Navbar';
import Signup from './Users/SignUp/Signup';
// import UploadImage from './Users/UploadImage/UploadImage';
import ALogin from './Admin/ALogin/ALogin';
import Patient from './Users/Patient/Patient';

function App() {
  return (
    <>
      <BrowserRouter>
      <Navbar />
      <Routes>

      <Route path="/" element={<Home />}></Route>
      <Route path="/login" element={<Login />}></Route>
      <Route path="/signup" element={<Signup />}></Route>
      {/* <Route path="/uploadImage" element={<UploadImage />}></Route> */}
      <Route path="/patients" element={<Patient/>}></Route>
      <Route path="/adminLogin" element={<ALogin />}></Route>
      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
