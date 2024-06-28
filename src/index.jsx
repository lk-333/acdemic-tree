import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';

import Login from './components/UserManagement/Login';
import Register from './components/UserManagement/Register'; 
import ForgetPassword from './components/UserManagement/ForgetPassword';

// import './styles.css';
import TeacherFunctionPage from './components/page/TeacherFunctionPage';  // 导入 TeacherFunctionPage 组件
import MyTreeComponent from "./components/MyTreeComponent";
import SearchPage from "./components/page/SearchPage";
import TeacherSearchPage from "./components/page/TeacherSearchPage";
import StudentSearchPage from "./components/page/StudentSearchPage";
import StudentFunctionPage from "./components/page/StudentFunctionPage";
import ViewApplicationPage from "./components/page/ViewApplicationPage";
import AdministerFunctionPage from "./components/page/AdministerFunctionPage"
import ViewAllApplicationsPage from "./components/page/ViewAllApplicationsPage"
import AdminiserSearchPage from "./components/page/AdministerSearchPage"

// 获取 root 元素
const container = document.getElementById('root');
const root = createRoot(container);

// 使用 createRoot 进行渲染
root.render(
    <React.StrictMode>

        <Router>
            <Routes>

                <Route path="/view-applications" element={<ViewApplicationPage  />} />
                <Route path="/view-allapplications" element={<ViewAllApplicationsPage />} />
                <Route path="/administer-function" element={<AdministerFunctionPage />} />
                <Route path="/teacher-function" element={<TeacherFunctionPage />} /> {/* 添加 TeacherFunctionPage 路由 */}
                <Route path="/student-function" element={<StudentFunctionPage />} />
                <Route path="/search-tree-administer" element={<AdminiserSearchPage  />} />
                <Route path="/search-tree-teacher" element={<TeacherSearchPage />} />
                <Route path="/search-tree-student" element={<StudentSearchPage />} />
                <Route path="/search-tree" element={<SearchPage />} /> {/* 添加 TreePage 路由 */}
                <Route path="/create-tree" element={<MyTreeComponent />} /> {/* 添加 TreePage 路由 */}
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forget_password" element={<ForgetPassword />} />
                {/* <Route path="/" element={<App />} /> */}
            </Routes>
        </Router>
    </React.StrictMode>
);
