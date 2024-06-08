import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = (e) => {
        e.preventDefault();
        // 简单存储用户名和密码到 localStorage
        if (username && password) {
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
            navigate('/login');
        } else {
            setError('请填写所有字段');
        }
    };

    return (
        <div className="register-container">
            <h2>注册</h2>
            <form onSubmit={handleRegister}>
                <div>
                    <label>账号:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>密码:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">注册</button>
            </form>
        </div>
    );
};

export default Register;
