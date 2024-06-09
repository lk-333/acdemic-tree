// Login.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './login.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [identity, setIdentity] = useState('student');
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
                // 将username赋值给Username
                const Username = username;

                // 根据身份跳转到不同页面并传递Username
                switch(identity) {
                    case 'student':
                        navigate('/search-tree-student', { state: { Username } });
                        break;
                    case 'teacher':
                        navigate('/search-tree-teacher', { state: { Username } });
                        break;
                    case 'admin':
                        navigate('/admin-dashboard', { state: { Username } });
                        break;
                    default:
                        navigate('/');
                        break;
                }
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
            <video autoPlay muted loop className="video-background">
                <source src="/videos/donghua.mp4" type="video/mp4"/>
            </video>
            <div className="card">
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
                    <div>
                        <label>身份:</label>
                        <select value={identity} onChange={(e) => setIdentity(e.target.value)}>
                            <option value="student">学生</option>
                            <option value="teacher">教师</option>
                            <option value="admin">管理员</option>
                        </select>
                    </div>
                    {error && <p className="error">{error}</p>}
                    <button type="submit">登录</button>
                </form>
                <p>还没有账号？ <Link to="/register">注册</Link></p>
            </div>
        </div>
    );
};

export default Login;
