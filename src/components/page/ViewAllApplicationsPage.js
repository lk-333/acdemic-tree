
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './ViewApplicationsPage.css';

const ViewAllApplicationsPage = () => {
    const [applications, setApplications] = useState([]);
    const [selectedApplication, setSelectedApplication] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [modalContent, setModalContent] = useState({});
    const navigate = useNavigate();
    const location = useLocation();
    const { Username } = location.state || {};

    const username = Username;


    const fetchApplications = async () => {
        try {
            const response = await fetch('/get-Allapplications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({  })

            });
            const data = await response.json();

            if (Array.isArray(data.applications)) {
                setApplications(data.applications);
            } else {
                console.error('Expected an array but received:', data);
                setApplications([]);
            }
        } catch (error) {
            alert('查看申请信息失败');
            console.error('Error fetching applications:', error);
        }
    };

    useEffect(() => {
        if (username) {
            fetchApplications();
        }
    }, [username]);

    const handleBack = () => {
        navigate('/administer-function');
    };

    const handleView = (app) => {
        setSelectedApplication(app);
        setModalContent(app);
        setShowModal(true);
    };

    const handleModalClose = () => {
        setShowModal(false);
    };

    const handleDecision = async (result) => {
        try {
            const response = await fetch('/deal-applications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ item_id: modalContent.item_id, result })
            });

            const data = await response.json();
            if (data.status === 1) {
                alert('操作成功');
                setShowModal(false);
                fetchApplications();  // 重新获取申请数据
            } else {
                alert('操作失败');
            }
        } catch (error) {
            alert('操作失败');
            console.error('Error dealing with application:', error);
        }
    };

    return (
        <div className="view-applications-container">
            <h1>查看申请</h1>
            <button onClick={handleBack} className="function-button">返回</button>

            <ul>
                {Array.isArray(applications) && applications.map((app, index) => (
                    <li
                        key={index}
                        onClick={() => handleView(app)}
                        className={selectedApplication?.item_id === app.item_id ? 'selected' : ''}
                    >
                        <p>申请人: {app.applicantName}</p>
                        <p>起止时间: {app.applicantTime}</p>

                    </li>
                ))}
            </ul>
            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleModalClose}>&times;</span>
                        <h2>申请详情</h2>
                        <p>申请人: {modalContent.applicantName}</p>
                        <p>起止时间: {modalContent.applicantTime}</p>
                        <p>是否同意此申请？</p>
                        <button onClick={() => handleDecision('Yes')} className="function-button">Yes</button>
                        <button onClick={() => handleDecision('No')} className="function-button">No</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ViewAllApplicationsPage;
