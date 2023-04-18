import React, { useState } from 'react';
import './ALogin.css';

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // const [modal, setModal] = useState(true);
  // const [error, setError] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    if (email === '' && password === '') {
      // setModal(!modal);
      alert("Please enter all the fields")
    }
  }

  return (
    <div className='Logbody'>
      <div className='Login'>
        <h1>Login</h1>
        <form>
          <label className="label">Email:</label>
          <input type="email" name="uname" id="uname" placeholder='Enter Email' /> <br /><br />
          <label className="label">Password:</label>
          <input type="password" name="password" id="pwd" placeholder='Enter Password' /> <br /> <br />
          <button onClick={handleLogin}>Submit</button><br /><br />
        </form>
      </div>
    </div>
  )
}

export default Login