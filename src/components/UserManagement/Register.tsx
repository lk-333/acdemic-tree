import React, { useState,useEffect } from 'react';
import { Input, Button, Form,Select } from 'antd';
import { useNavigate, Link } from 'react-router-dom';
import './UserManagement.css';

import VerificationCodeButton from "./VerificationCodeButton";



const checkUsernameAvailability = async (username) => {
    const response = await fetch('/api/userAvailability', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
    });
    const data = await response.json();
    return data.isAvailable; 
};

function UsernameInput(){
    return ( 
        <Form.Item
            name="username"
            rules={[
                { required: true, message: '请输入用户名' },
                {
                    pattern: /^(?:\d+|[a-zA-Z]+|[a-zA-Z\d]+)$/i,
                    message: '用户名为纯数字、纯英文字母或数字与英文字母组合',
                },
                () => ({
                    validator: async (_, username) => {
                        if (!username) return Promise.resolve();
                        const isAvailable = await checkUsernameAvailability(username);
                        if (!isAvailable) {
                            return Promise.reject(new Error('该用户名已被使用'));
                        }
                        return Promise.resolve();
                    },
                }),
            ]}
        >
            <Input placeholder="请输入用户名" />
        </Form.Item>
    );
};


const Register = () => {
    const [form] = Form.useForm();
    const [isCodeButtonDisabled, setIsCodeButtonDisabled] = useState(true);
    const { Option } = Select;
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (values) => {
        console.log(values);
        const {email,identity,password,username,verificationCode}=values;
        if(verificationCode!=="1234")
        {
            setError("验证码错误")
        }
        else if (username && password && identity) {
            try {
                const response = await fetch('/api/register_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password, identity }),
                });
                const data = await response.json();
                navigate('/');
            } catch (err) {
                console.error('Error:', err);
                setError('服务器错误');
            }
        } 
    };
    
    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const email = e.target.value;
        // 使用正则表达式来验证邮箱格式
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        // 检查邮箱是否匹配正则表达式
        setIsCodeButtonDisabled(!emailPattern.test(email));
    };


    return (
        <div className="form_container">
            <video autoPlay muted loop className="video-background">
                <source src="path/to/your/video.mp4" type="video/mp4" />
                您的浏览器不支持视频标签。
            </video>
            <Form form={form} onFinish={handleSubmit} className="custom_form">
                <h2>用户注册</h2>
                
                <UsernameInput />

                <Form.Item
                    name="email"
                    rules={[
                        { required: true, message: '请输入邮箱' },
                        {
                            pattern: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/,
                            message: '请输入有效的邮箱',
                        },
                    ]}
                >
                    <Input placeholder="请输入邮箱" onChange={handleEmailChange} />
                </Form.Item>
                <div className='verificationArea'>
                    <Form.Item
                        name="verificationCode"
                        className='verificationCode'
                        rules={[{ required: true, message: '请输入验证码' }]}
                    >
                        <Input placeholder="请输入验证码"/>
                    </Form.Item>
                    
                    <VerificationCodeButton 
                            isCodeButtonDisabled={isCodeButtonDisabled}
                            setIsCodeButtonDisabled={setIsCodeButtonDisabled}
                        />

                </div>
                <Form.Item
                    name="password"
                    rules={[
                        { required: true, message: '请输入密码' },
                        { min: 6, message: '密码最少6位' },
                        {
                            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/,
                            message: '密码需包含至少1个大写字母、1个小写字母、1个数字和1个特殊字符',
                        },
                    ]}
                >
                    <Input.Password placeholder="请输入密码"/>
                </Form.Item>

                <Form.Item
                    name="password_again"
                    dependencies={['password']}  // 添加依赖，当密码字段变化时重新验证
                    rules={[
                        {
                            required: true,
                            message: '请再次输入密码',
                        },
                        ({ getFieldValue }) => ({
                            validator(_, value) {
                                if (!value || getFieldValue('password') === value) {
                                    return Promise.resolve();
                                }
                                return Promise.reject(new Error('两次输入的密码不一致'));
                            },
                        }),
                    ]}
                >
                    <Input.Password placeholder="请再次输入密码"/>
                </Form.Item>
                
                <Form.Item
                    name="identity"
                    rules={[
                        { required: true, message: '请选择身份' },
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
                        立即注册
                    </Button>
                </Form.Item>
                <div className='toRouter'>
                    <Link to="/forget_password">忘记密码</Link>
                    <span>已有账号?<Link to="/" >马上登录</Link></span>
                </div>
            </Form>
        </div>
    );
};

export default Register;
