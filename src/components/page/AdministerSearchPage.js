import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {useLocation, useNavigate} from 'react-router-dom';
import './SearchPage.css';  // 引入样式文件

const AdminiserSearchPage = () => {
    const [name, setName] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const { Username  } = location.state || {};



    const handleSearch = async () => {

        // 发送请求到后端，你可以使用 fetch 或 axios 发送请求
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
                navigate('/create-tree?id=111');



            } else {
                alert('搜索失败');
                console.error('搜索失败');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleAdministerFunctionClick = () => {
        navigate('/administer-function', { state: { Username  } });
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

                <button onClick={handleSearch} className="search-button">搜索</button>

            </div>



            <div className="sidebar">
                <div className="sidebar-logo">
                    <div className="logo-container">
                        <img src="/photo/logo.png" alt="Logo"/>
                    </div>

                </div>
                <ul className="sidebar-menu">
                    <li><a onClick={handleAdministerFunctionClick}>管理员功能</a></li>
                    <li><a onClick={handleAdministerFunctionClick}>文献资源</a></li>
                    <li><Link to="/login">退出登录</Link></li>
                </ul>
                <div className="sidebar-footer">
                    <button>我的导航</button>
                </div>
            </div>

        </div>
    );
};

export default AdminiserSearchPage;
