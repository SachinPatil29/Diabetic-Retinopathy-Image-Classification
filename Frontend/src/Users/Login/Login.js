import axios from 'axios';
import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {

  const [Values, setdata] = useState({
    username: "",
    password: "",
  })
  const navigate = useNavigate();
  const setVal = (event) => {
    const name = event.target.name;
    const value = event.target.value;

    setdata((prev) => {
      return { ...prev, [name]: value }
    })
  }
  const handleLogin = async (e) => {
    e.preventDefault();

    const userdata = {
      username: Values.username,
      password: Values.password
    }
    console.log(userdata);
    const {username, password} = Values;

    if (Values.username === '' || Values.password === '') {
      alert("Please enter all the fields");
    }
    else {
      try{
        const response = await axios.post("http://127.0.0.1:8000/api/login/", {username, password});
        if(response.status === 200){
          const token = response.data.token;
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;
          console.log(token)
          alert("Logged in successfully");
          navigate('/patients');
        }
        else{
          alert("Error", response.status);
        }
      }catch(error){
        alert("Invalid credentials");
      }
    }
  }


  return (
    <div className='Logbody'>
      <div className='Login'>
        <h1>Login</h1>
        <form>
          <label className="label">Username:</label>
          <input type="email" name="username" id="username" placeholder='Enter Username' value={Values.username} onChange={setVal} /> <br /><br />
          <label className="label">Password:</label>
          <input type="password" name="password" id="password" placeholder='Enter Password' value={Values.password} onChange={setVal} /> <br /> <br />
          <button onClick={handleLogin}>Submit</button><br /><br />
        </form>
      </div>
    </div>
  )
}

export default Login