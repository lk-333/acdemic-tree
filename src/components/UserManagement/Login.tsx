import React, { useState } from 'react';
import { Input, Button, Form,Select } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import './UserManagement.css';



const Login = () => {
    const [form] = Form.useForm();
    const { Option } = Select;
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (values) => {
        
        const { username, password, identity } = values;
        // console.log(username);
        try {
            const response = await fetch('/api/check_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, identity }),
            });

            const data = await response.json();
            console.log(data)
            if (data.status === 1) {
                // 将username赋值给Username
                const Username = username;

                // 根据身份跳转到不同页面并传递Username
                switch(identity) {
                    case 'student':
                        navigate('/search-tree-student', { state: { Username } });
                        break;
                    case 'teacher':
                        navigate('/search-tree-teacher', { state: { Username } });
                        break;
                    case 'admin':
                        navigate('/admin-dashboard', { state: { Username } });
                        break;
                    default:
                        navigate('/');
                        break;
                }
            } else if (data.status === -1) {
                setError('用户不存在');
            } else if (data.status === 0) {
                setError('密码错误');
            }
        } catch (err) {
            console.error('Error:', err);
            setError('服务器错误');
        }
    };



    return (
        <div className="form_container">
            <video autoPlay muted loop className="video-background">
                <source src="/videos/donghua.mp4" type="video/mp4"/>
            </video>
            <Form form={form} onFinish={handleLogin} className="custom_form">
                <h2>登录</h2>
                <Form.Item
                    name="username"
                    rules={[
                        {required: true, message: '请输入用户名或邮箱'},
                    ]}
                >
                    <Input placeholder="请输入用户名或邮箱"/>
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[
                        {required: true, message: '请输入密码'},
                    ]}
                >
                    <Input.Password placeholder="请输入密码"/>
                </Form.Item>

                <Form.Item
                    name="identity"
                    rules={[
                        {required: true, message: '请选择身份'},
                    ]}
                >
                    <Select placeholder="请选择身份">
                        <Option value="teacher">老师</Option>
                        <Option value="student">学生</Option>
                        <Option value="admin">管理员</Option>
                    </Select>
                </Form.Item>

                {error && <p className="error">{error}</p>}

                <Form.Item>
                    <Button type="primary" htmlType="submit" className='submitButton'>
                        登录
                    </Button>
                </Form.Item>
                <div className='toRouter'>
                    <Link to="/forget_password">忘记密码</Link>
                    <span>已有账号?<Link to="/register">快速注册</Link></span>
                </div>

            </Form>

        </div>

    );
};

export default Login;
