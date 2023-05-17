import axios from 'axios';
import React, { useState } from 'react';
import './RetrainModel.css';

function RetrainModel () {
  const [training, setTraining] = useState(false);

  const handleTrainClick = () => {
    setTraining(true);
    console.log("training...");
    axios.post('http://127.0.0.1:8000/api/retrainModel/').then(() => {
      console.log("training completed...");
      setTraining(false);
      alert('Training successful!');
    }).catch(() => {
      setTraining(false);
      // alert('Training failed!');
      alert('Training...');
    });
  }
  
  return (
    <button onClick={handleTrainClick}>Retrain Model</button>
  );
}
export default RetrainModel