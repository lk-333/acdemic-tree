import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [identity, setIdentity] = useState('');

    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/check_user', { username, password,identity });
            const { status } = response.data;
            if (status === 1) {
                navigate('/');
            }
            else if(status === -1)
            {
            //     用户不存在
            }
            else if(response.status === 0)
            {
                //     密码错误
            }
        } catch (err) {
            setError('密码错误');
        }
    };

    return (
        <div className="login-container">
            <h2>登录</h2>
            <form onSubmit={handleLogin}>
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
                <button type="submit">登录</button>
            </form>
            <p>还没有账号？ <Link to="/register">注册</Link></p>
        </div>
    );
};

export default Login;
