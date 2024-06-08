import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [identity, setIdentity] = useState('student');  // 添加用户身份状态，默认为 'student'
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        if (username && password && identity) {
            try {
                const response = await fetch('/register_user', {  // 假设后端路由为 '/register_user'
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password, identity }),
                });
                const data = await response.json();
                if (data.status === 1) {
                    navigate('/login');
                } else {
                    setError('注册失败，请重试');
                }
            } catch (err) {
                console.error('Error:', err);
                setError('服务器错误');
            }
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
                <div>
                    <label>身份:</label>
                    <select value={identity} onChange={(e) => setIdentity(e.target.value)}>
                        <option value="student">学生</option>
                        <option value="teacher">老师</option>
                        <option value="admin">管理员</option>
                    </select>
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">注册</button>
            </form>
        </div>
    );
};

export default Register;
