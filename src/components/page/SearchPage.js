// SearchPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchPage.css';  // 引入样式文件

const SearchPage = () => {
    const [name, setName] = useState('');
    const navigate = useNavigate();

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
                navigate('/create-tree');
            } else {
                console.error('搜索失败');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleTeacherFunctionClick = () => {
        navigate('/teacher-function');
    };


    return (
        <div className="search-container">
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="请输入名字"
                className="search-input"
            />

            <button onClick={handleSearch} className="search-button">Search</button>
            <button onClick={handleTeacherFunctionClick} className="teacher-function-button">教师功能</button>

        </div>
    );
};

export default SearchPage;
