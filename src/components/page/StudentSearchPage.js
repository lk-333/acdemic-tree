import React, { useState } from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import './SearchPage.css';  // 引入样式文件

const StudentSearchPage = () => {
    const [name, setName] = useState('');
    const navigate = useNavigate();

    const location = useLocation();
    const { username } = location.state || {};


    const handleLogout = () => {
        navigate('/login');
    };

    const handleStudentSearch = async () => {
        // 发送请求到后端，使用 fetch 或 axios 发送请求
        try {
            const response = await fetch('/search_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name })
            });

            const data = await response.json();

            if (data.status === 1) {
                // 假设后端返回了成功的响应，跳转到创建树的页面
                navigate('/create-tree');
            } else {
                console.error('搜索失败');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleStudentFunctionClick = () => {
        navigate('/student-function', { state: { username } });
    };

    return (
        <div className="search-container">
            <video autoPlay muted loop className="video-background">
                <source src="/videos/sea.mp4" type="video/mp4"/>
            </video>
            <div className="content-wrapper">
                <h1 className="title">学术师承树</h1>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="请输入名字"
                    className="search-input"
                />
                <button onClick={handleStudentSearch} className="search-button">搜索</button>
                <button onClick={handleStudentFunctionClick} className="teacher-function-button">学生功能</button>
                <button className="logout-button" onClick={handleLogout}>退出登录</button>
            </div>
        </div>
    );
};

export default StudentSearchPage;
