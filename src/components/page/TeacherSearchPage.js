import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {useLocation, useNavigate} from 'react-router-dom';
import './SearchPage.css';  // 引入样式文件

const TeacherSearchPage = () => {
    const [name, setName] = useState('');
    const [searchType, setSearchType] = useState('Name');
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
                body: JSON.stringify({ name, type: searchType })
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
            alert('搜索出错');
        }
    };

    const handleTeacherFunctionClick = () => {
        navigate('/teacher-function', { state: { Username  } });
    };

    return (
        <div className="search-container">
            <video autoPlay muted loop className="video-background">
                <source src="/videos/sea.mp4" type="video/mp4"/>
            </video>
            <div className="content-wrapper">
                <h1 className="title">学术师承树</h1>
                <div className="search-bar">

                    <select value={searchType} onChange={(e) => setSearchType(e.target.value)}
                            className="search-select">
                        <option value="Name">人名</option>
                        <option value="Institution">机构</option>
                        {/* 可以根据需要添加更多搜索类型 */}
                    </select>

                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="请输入名字"
                        className="search-input"
                    />

                    <button onClick={handleSearch} className="search-button">搜索</button>

                </div>
            </div>


            <div className="sidebar">
                <div className="sidebar-logo">
                    <div className="logo-container">
                        <img src="/photo/logo.png" alt="Logo"/>
                    </div>

                </div>
                <ul className="sidebar-menu">
                <li><a onClick={handleTeacherFunctionClick}>教师功能</a></li>
                    <li><a onClick={handleTeacherFunctionClick}>文献资源</a></li>
                    <li><Link to="/">退出登录</Link></li>
                </ul>
                <div className="sidebar-footer">
                <button>我的导航</button>
                </div>
            </div>

        </div>
    );
};

export default TeacherSearchPage;
