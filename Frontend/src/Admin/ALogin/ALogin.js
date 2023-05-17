import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ALogin.css';

const Login = () => {

 const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/adminLogin/", { username, password });
      if(response.status === 200){
        const token = response.data.token;
        axios.defaults.headers.common['Authorization'] = `Token ${token}`;
        console.log(token)
        alert("Logged in successfully");
        localStorage.setItem("auth", token);
        navigate('/dashboard');
      }
      else{
        alert("Error", response.status);
      }
    }catch(error){
      alert("Invalid credentials");
    }
  };


  return (
    <div className='loginbody'>
      <div className='Login'>
        <h1>Login</h1>
        <form onSubmit={handleSubmit}>
          <label className="label">Username:</label>
          <input type="text" name="username" id="username" placeholder='Enter Username' value={username} onChange={(event) => setUsername(event.target.value)} /> <br /><br />
          <label className="label">Password:</label>
          <input type="password" name="password" id="password" placeholder='Enter Password' value={password} onChange={(event) => setPassword(event.target.value)} /> <br /> <br />
          {error && <div>{error}</div>}
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  )
}

export default Login