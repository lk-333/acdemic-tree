import React from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import './TeacherFunctionPage.css';

const AdministerFunctionPage = () => {
    const navigate = useNavigate();


    const location = useLocation();
    const { Username } = location.state || {};


    const handleViewApplications = () => {
        navigate('/view-allapplications', { state: { Username } });
    };

    const handleBack = () => {
        navigate('/search-tree-administer');
    };

    const handleLogout = () => {
        navigate('/login');
    };




    return (
        <div className="teacher-function-container">
            <video autoPlay muted loop className="video-background">
                <source src="/videos/snow.mp4" type="video/mp4"/>
            </video>
            <div className="content-wrapper">
                <h1 className="title">管理员功能页面</h1>
                <button onClick={handleViewApplications} className="function-button">查看申请</button>
                <button onClick={handleBack} className="function-button">返回</button>

            </div>
        </div>
    );
};

export default AdministerFunctionPage;
