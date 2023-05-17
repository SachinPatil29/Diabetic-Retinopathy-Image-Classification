import React, { useState, useEffect } from 'react'

const PatientDetails = (props) => {

    // const [patients, setPatients] = useState([]);

    // useEffect(() => {
    //   async function fetchPatients() {
    //     const response = await fetch('http://127.0.0.1:8000/api/patientDetails/');
    //     const data = await response.json();
    //     setPatients(data.data);
    //   }
    //   fetchPatients();
    // }, []);
    
    // const handleImageClick = (imageUrl) => {
    //     window.open(imageUrl, '_blank');
    //   }


    const [patient, setPatient] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Send a GET request to the backend API with the patient ID
    fetch(`http://127.0.0.1:8000/api/patients/${props.match.params.patientId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
          setPatient(null);
        } else {
          setPatient(data);
          setError(null);
        }
      })
      .catch(error => {
        setError('Error fetching patient data');
        setPatient(null);
      });
  }, [props.match.params.patientId]);

  if (error) {
    return <div>{error}</div>;
  } else if (!patient) {
    return <div>Loading patient data...</div>;
  }


  return (
    <div>
        {/* <table>
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
      
      {patients.forEach(patient => (
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
      <tr key={patients.id}>
            <td>{patients.id}</td>
            <td>{patients.first_name}</td>
            <td>{patients.last_name}</td>
            <td>{patients.age}</td>
            <td>{patients.gender}</td>
            <td>{patients.phone_number}</td>
            <td>
              <button onClick={() => handleImageClick(patients.image)}>
                {patients.image}
              </button>
            </td>
            <td>{patients.prediction}</td>
          </tr>
      </tbody>
        </table> */}



        <div>
      <h1>{patient.fname} {patient.lname}</h1>
      <p>Age: {patient.age}</p>
      <p>Gender: {patient.gender}</p>
      <p>Phone number: {patient.phonenumber}</p>
      <img src={patient.image} alt="Patient image" />
      <p>Labels: {patient.labels.join(', ')}</p>
    </div>
    </div>
  )
}

export default PatientDetails