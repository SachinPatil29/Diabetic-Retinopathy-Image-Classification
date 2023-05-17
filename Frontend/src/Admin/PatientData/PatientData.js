import React, { useState, useEffect } from 'react';
// import './UserData.css';

function PatientData () {

    const [patients, setPatients] = useState([]);

    useEffect(() => {
      async function fetchPatients() {
        const response = await fetch('http://127.0.0.1:8000/api/patientData/');
        const data = await response.json();
        setPatients(data.data);
      }
      fetchPatients();
    }, []);
    
    const handleImageClick = (imageUrl) => {
        window.open(imageUrl, '_blank');
      }

      return (
    <div className='ptable'>
       <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Age</th>
          <th>Gender</th>
          <th>Phone Number</th>
          <th>Image</th>
          <th>Prediction</th>
        </tr>
      </thead>
      <tbody>
        {patients.map(patient => (
          <tr key={patient.id}>
            <td>{patient.id}</td>
            <td>{patient.first_name}</td>
            <td>{patient.last_name}</td>
            <td>{patient.age}</td>
            <td>{patient.gender}</td>
            <td>{patient.phone_number}</td>
            <td>
              <button onClick={() => handleImageClick(patient.image)}>
                {patient.image}
              </button>
            </td>
            <td>{patient.prediction}</td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
  )
}

export default PatientData