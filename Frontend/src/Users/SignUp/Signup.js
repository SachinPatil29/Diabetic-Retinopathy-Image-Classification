import React, { useState } from 'react';
import axios from 'axios';
import './Signup.css';
import { useNavigate } from 'react-router-dom';

const Signup =()=>{
    const [Values, setdata] = useState({
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      password: "",
      password2: ""
    })
    const navigate = useNavigate();
  
    const setVal = (e) => {
      // const {name,value} = e.target;
      const name = e.target.name;
      const value = e.target.value;
      // event.preventDefault();
  
      // setdata({...data,[name]:value})
      setdata((prev) => {
        return { ...prev, [name]: value }
      })
    }
  
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      if (Values.password === Values.password2) {
        const userdata2 = {
          first_name: Values.first_name,
          last_name: Values.last_name,
          username: Values.username,
          email: Values.email,
          password: Values.password,
          password2: Values.password2,
        }
        console.log(userdata2);
        // console.log("user data defined")
  
        axios.post("http://127.0.0.1:8000/api/register/", userdata2)
        .then((res)=>{
            console.log("register successfully",res)
            alert("Your Sign Up is successfull")
            navigate('/login')
        })
        .catch((error)=>{
            console.log("Already registered",error)
        })
      }
      else {
        alert("Password does not match")
      }
    }

  return (
    <div className="form">
        <div>
            <h1>Sign Up</h1>
        </div>
        <div>
        <form onSubmit={handleSubmit}>
                <label className="label">Firstname:</label>
                <input type="text" className='input' placeholder="Enter Firstname" name="first_name" value={Values.first_name} onChange={setVal} /> <br /> <br />

                <label className="label">Lastname:</label>
                <input type="text" className='input' placeholder="Enter Lastname" name="last_name" value={Values.last_name} onChange={setVal} /> <br /> <br />

                <label className="label">Username:</label>
                <input type="text" className='input' placeholder="Enter Username" name="username" value={Values.username} onChange={setVal} /> <br /> <br />

                <label className="label">Email:</label>
                <input type="email" className='input' placeholder="Enter email" name="email" value={Values.email} onChange={setVal} /> <br /><br />

                <label className="label">Password:</label>
                <input type="password" className='input' placeholder="Enter password" name="password" value={Values.password} onChange={setVal} /> <br /><br />

                <label className="label">Confirm Password:</label>
                <input type="password" className='input' placeholder="Enter confirm password" name="password2" value={Values.password2} onChange={setVal} /> <br /><br />

                <button type="submit" className="btn">Submit</button>
            </form>
        </div>
    </div>
  )
}

export default Signup