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
import RetrainModel from './Admin/RetrainModel/RetrainModel';
import UserData from './Admin/UserData/UserData';
import PatientData from './Admin/PatientData/PatientData';
import Dashboard from './Admin/Dashboard/Dashboard';
import PatientDetails from './Users/PatientDetails/PatientDetails';
// import AdminNavbar from './Admin/AdminNavbar/AdminNavbar';

function App() {

  const auth = localStorage.getItem('admin');
  return (
    <>
      <BrowserRouter>
      <Navbar />
      {/* <AdminNavbar /> */}
      <Routes>

      <Route path="/" element={<Home />}></Route>
      <Route path="/login" element={<Login />}></Route>
      <Route path="/signup" element={<Signup />}></Route>
      {/* <Route path="/uploadImage" element={<UploadImage />}></Route> */}
      <Route path="/patients" element={<Patient/>}></Route>
      <Route path="/adminLogin" element={<ALogin />}></Route>
      <Route path="/users" element={<UserData />}></Route>
      <Route path="/patientData" element={<PatientData />}></Route>
      <Route path="/retrainModel" element={<RetrainModel />}></Route>
      <Route path="/dashboard" element={<Dashboard />}></Route>
      <Route path="/patientDetails" element={<PatientDetails />}></Route>
      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
