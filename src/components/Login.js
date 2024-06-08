import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../styles.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [identity, setIdentity] = useState('admin');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/check_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, identity }),
            });


            const data = await response.json();

            if (data.status === 1) {
                navigate('/');
            } else if (data.status === -1) {
                setError('用户不存在');
            } else if (data.status === 0) {
                setError('密码错误');
            }
        } catch (err) {
            console.error('Error:', err);
            setError('服务器错误');
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
