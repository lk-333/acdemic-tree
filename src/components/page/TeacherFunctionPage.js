import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './TeacherFunctionPage.css';

const TeacherFunctionPage = () => {
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);
    const [yourName, setYourName] = useState('');
    const [otherName, setOtherName] = useState('');
    const [yourRole, setYourRole] = useState('');
    const [otherRole, setOtherRole] = useState('');

    const handleViewApplications = () => {
        navigate('/view-applications');
    };

    const handleBack = () => {
        navigate('/search-tree-teacher');
    };

    const handleLogout = () => {
        navigate('/login');
    };

    const handleOpenModal = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    const handleSubmit = async () => {
        try {
            const response = await fetch('/send-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ yourName, otherName, yourRole, otherRole })
            });

            const data = await response.json();

            if (data.status === 1) {
                alert("申请已发送");
            } else {
                alert("发送失败");
                console.error('搜索失败');
            }
        } catch (error) {
            console.error('Error:', error);
        }
        setShowModal(false); // 关闭模态窗口
    };


    return (
        <div className="teacher-function-page">
            <div className="buttons-container">
                <h1>教师功能页面</h1>
                <button onClick={handleViewApplications}>查看申请</button>
                <button onClick={handleOpenModal}>发送申请</button>
                {showModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <span className="close" onClick={handleCloseModal}>&times;</span>
                            <h2>发送申请</h2>
                            <input
                                type="text"
                                placeholder="请输入你的名字"
                                value={yourName}
                                onChange={(e) => setYourName(e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder="请输入对方的名字"
                                value={otherName}
                                onChange={(e) => setOtherName(e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder="请输入你的身份"
                                value={yourRole}
                                onChange={(e) => setYourRole(e.target.value)}
                            />
                            <input
                                type="text"
                                placeholder="请输入对方的身份"
                                value={otherRole}
                                onChange={(e) => setOtherRole(e.target.value)}
                            />
                            <button onClick={handleSubmit}>提交</button>
                        </div>
                    </div>
                )}
                <button onClick={handleBack}>返回</button>
                <button className="logout-button" onClick={handleLogout}>退出登录</button>
            </div>
        </div>
    );
};

export default TeacherFunctionPage;
