import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
// import RetrainModel from '../RetrainModel/RetrainModel';
import './Dashboard.css';

function Dashboard() {

  const navigate = useNavigate();
  const [showRetrainModel, setShowRetrainModel] = useState(false);

  const handleUserSubmit = (e) => {
    e.preventDefault();
    navigate('/users');
  }

  const handlePatientSubmit = (e) => {
    e.preventDefault();
    navigate('/patientData');
  }

  const handleRetrainSubmit = (e) => {
    e.preventDefault();
    navigate('/retrainModel');
    setShowRetrainModel(true);
  }


  // const [training, setTraining] = useState(false);

  // function handleTrainClick() {
  //   setTraining(false);
  //   axios.post('http://127.0.0.1:8000/api/retrainModel/').then(() => {
  //     setTraining(true);
  //     alert('Training successful!');
  //   }).catch(() => {
  //     setTraining(true);
  //     alert('Training failed!');
  //   });
  // }


  return (
    <div>
      <div className='dashboard1'>
        <form>
          <button type='submit' onClick={handleUserSubmit}>All Users</button> {" "}<br />
          <button type='submit' onClick={handlePatientSubmit}>All Patients</button>{" "} <br />
          <button type='submit' onClick={handleRetrainSubmit}>Retrain</button> {" "}<br />
        </form>
      </div>

      {/* {showRetrainModel && <RetrainModel />} */}
    </div>
  )
}

export default Dashboard