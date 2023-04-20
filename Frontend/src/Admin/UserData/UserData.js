import React, { useState, useEffect } from 'react';
import './UserData.css';

function UserData() {

    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/users/')
            .then(response => response.json())
            .then(data => setUsers(data.data));
    }, []);


    return (
        <div className='body1'>
        <div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Username</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.id}</td>
                            <td>{user.first_name}</td>
                            <td>{user.last_name}</td>
                            <td>{user.username}</td>
                            <td>{user.email}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
        </div>
    )
}

export default UserData

