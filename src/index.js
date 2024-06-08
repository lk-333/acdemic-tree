import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import Login from './components/Login';
import Register from './components/Register'; // 导入 Register 组件
import './styles.css';

// 获取 root 元素
const container = document.getElementById('root');
const root = createRoot(container);

// 使用 createRoot 进行渲染
root.render(
    <React.StrictMode>
        <Router>
            <Routes>

                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/" element={<App />} />
            </Routes>
        </Router>
    </React.StrictMode>
);
