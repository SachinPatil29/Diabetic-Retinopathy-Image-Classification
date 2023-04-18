import React, { useState } from 'react';
import './Patient.css';

function Patient() {
  const [patientData, setPatientData] = useState({
    first_name: '',
    last_name: '',
    age: '',
    gender: '',
    phone_number: '',
    image: null
  });

  function handleSubmit(event) {
    event.preventDefault();

    // Create a FormData object and append patient data and image file
    const formData = new FormData();
    formData.append('first_name', patientData.first_name);
    formData.append('last_name', patientData.last_name);
    formData.append('age', patientData.age);
    formData.append('gender', patientData.gender);
    formData.append('phone_number', patientData.phone_number);
    formData.append('image', patientData.image);

    // Send a POST request to Django API endpoint
    fetch('http://127.0.0.1:8000/api/patients/', {
      method: 'POST',
      body: formData
    })
      // .then(response => response.json())
      // .then(data => console.log(data))
      // alert('Patient data stored successfully!');
      // navigate('/response')
      .then((response) => {
        // setLabel(response.data.label);
        response.json()
        console.log(response.data);
        alert('Patient data stored successfully!');
        // navigate('/response')
      })
      .catch(error => console.error(error));
  }

  function handleInputChange(event) {
    const { name, value } = event.target;
    setPatientData(prevState => ({
      ...prevState,
      [name]: value
    }));
  }

  function handleImageChange(event) {
    setPatientData(prevState => ({
      ...prevState,
      image: event.target.files[0]
    }));
  }

  return (
    <div className='body'>
      <h1>Enter the Patient Details</h1>
      <div>
        {/* <form onSubmit={handleSubmit}>
                    <label className='label'>Firstname:</label>
                        <input type="text" name="first_name" placeholder='Enter first name' id="first_name" value={patientData.first_name } onChange={handleInputChange } />
                     <br />
                    <label className='label'>Lastname:
                        <input type="text" name="last_name" id="last_name" placeholder='Enter last name' value={patientData.last_name} onChange={handleInputChange} /> </label> <br />
                    <label className='label'>Age:
                        <input type="text" name="age" id="age" placeholder='Enter age' value={patientData.age} onChange={handleInputChange} /></label> <br />
                    <label className='label'>Gender:
                        <select name="gender" id="gender" value={patientData.gender} onChange={handleInputChange}>
                            <option value="select">Select</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                        </select> </label><br />
                    <label className='label'>Phone Number:
                        <input type="number" name="phone_number" id="phone_number" placeholder='Enter Phone number' value={patientData.phone_number} onChange={handleInputChange} /></label> <br />

                    <div className='preview'>
                        <input type="file" name='image' accept="image/*" onChange={handleImageChange} required /> <br />
                        <img src={patientData.image} width={"30%"} height={"30%"} />
                    </div>
                    <button className='btn' type='submit'>Submit</button>

                </form> */}
        <form onSubmit={handleSubmit}>
          <label htmlFor="first_name" className='label'>Firstname:
            <input type="text" name="first_name" id="first_name" placeholder='Enter the Firstname' value={patientData.first_name} onChange={handleInputChange} />
          </label> <br />

          <label htmlFor="last_name" className='label'>Lastname:
            <input type="text" name="last_name" id="last_name" placeholder='Enter the Lastname' value={patientData.last_name} onChange={handleInputChange} />
          </label> <br />

          <label htmlFor="age" className='label'>Age:
            <input type="number" name="age" id="age" placeholder='Enter the age' value={patientData.age} onChange={handleInputChange} />
          </label> <br />

          <label className='label'>Gender:
            <select name="gender" id="gender" value={patientData.gender} onChange={handleInputChange}>
              <option value="select">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select> </label><br />

          <label htmlFor="phone_number" className='label'>Phone Number:
            <input type="text" name="phone_number" id="phone_number" placeholder='Enter Phone number' value={patientData.phone_number} onChange={handleInputChange} />
          </label> <br />

          <div className='preview'>
            <input type="file" name='image' accept="image/*" onChange={handleImageChange} required /> <br />
            {/* <img src={patientData.image} width={"30%"} height={"30%"} /> */}
          </div>
          <button className='btn' type='submit'>Submit</button>
        </form>
      </div>
    </div>
  )
}

export default Patient