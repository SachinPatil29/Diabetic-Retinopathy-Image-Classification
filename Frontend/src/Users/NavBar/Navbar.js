import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import kle_logo from '../images/kletech_logo.png';
// import HPC_logo from '../images/HPC_logo.jpg';
import { toast } from 'react-toastify';
import { Bounce } from 'react-toastify';
import './Navbar.css';

const Navbar = () => {
    const navigate = useNavigate();
    const auth = localStorage.getItem('user');
    const logout = () => {
        localStorage.clear();
        toast.success("You have successfully logged out!",{
            transition:Bounce
        });
        navigate("/login");
    }
  return (
    <nav>
        <img src={kle_logo} className='img1' width={"20%"} height={"60%"} />
        <div id='top-right'>
            {
                auth? <>
                    <Link className='bar1' to="/dashboard">Dashboard</Link>  
                    <Link className="bar1" to="/about">About</Link>
                    <Link className="bar1" to="/contact">Contact</Link>
                    <Link onClick={logout} className="bar1" to="/login">Logout</Link>
                </> : <>
                    <Link className="bar1" to="/">Home</Link>
                    <Link className="bar1" to="/login">Login</Link>
                    <Link className="bar1" to="/adminLogin">Admin</Link>
                    <Link className="bar1" to="/signup">Sign Up</Link>
                </>
            }
        </div>
    </nav>
  )
}

export default Navbar