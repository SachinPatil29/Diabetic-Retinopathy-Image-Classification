import React, { useState } from 'react';
import axios from 'axios';

function RetrainModel () {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
      };

      const handleFileSubmit = async (event) => {
        event.preventDefault();
        if (file) {
          const formData = new FormData();
          formData.append('file', file);
          try {
            const response = await axios.post('http://127.0.0.1:8000/api/retrainModel/', formData, {
              headers: { 'Content-Type': 'multipart/form-data' },
            });
            setMessage(response.data.success);
          } catch (error) {
            setMessage(error.response.data.error);
          }
        }
      };

  return (
    <div>
        <form onSubmit={handleFileSubmit}>
            <label htmlFor="images">
                <input type="file" name="image_file" id="image_file" onChange={handleFileChange} />
            </label>
            <button type='submit'>Retrain Model</button>
        </form>
        <p>{message}</p>
    </div>
  )
}

export default RetrainModel