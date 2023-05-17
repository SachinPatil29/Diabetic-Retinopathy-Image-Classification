import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import kle_logo from '../Images/kletech_logo.png';
// import HPC_logo from '../images/HPC_logo.jpg';
import { toast } from 'react-toastify';
import { Bounce } from 'react-toastify';

const AdminNavbar = () => {
    const navigate = useNavigate();
    const auth = localStorage.getItem('auth');
    const logout = () => {
        localStorage.clear();
        toast.success("You have successfully logged out!",{
            transition:Bounce
        });
        navigate("/adminLogin");
    }
  return (
    <div>
        <nav>
        <img src={kle_logo} className='img1' width={"20%"} height={"60%"} />
        <div id='top-right'>
            {
                auth? <>
                    <Link className='bar2' to="/dashboard">Dashboard</Link>  
                    <Link className='bar2' to="/users">Users</Link>  
                    {/* <Link className="bar2" to="/about">About</Link>
                    <Link className="bar2" to="/contact">Contact</Link> */}
                    <Link onClick={logout} className="bar2" to="/login">Logout</Link>
                </> : <>
                    <Link className="bar2" to="/">Home</Link>
                    <Link className="bar2" to="/login">Login</Link>
                    {/* <Link className="bar2" to="/adminLogin">Admin</Link> */}
                    <Link className="bar2" to="/signup">Sign Up</Link>
                </>
            }
        </div>
    </nav>
    </div>
  )
}

export default AdminNavbar