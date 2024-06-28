import React, { useState } from 'react';
import { Input, Button, Form } from 'antd';
import { Link } from 'react-router-dom';
import './UserManagement.css';
import VerificationCodeButton from "./VerificationCodeButton";

const ForgetPassword = () => {
    const [form] = Form.useForm();
    const [isCodeButtonDisabled, setIsCodeButtonDisabled] = useState(true);

    const handleSubmit = (values: any) => {
        // 验证通过后的处理逻辑，可以将表单数据存储至React Redux和localStorage
        console.log(values);
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
            <Form form={form} onFinish={handleSubmit}  className="custom_form">
                <h2>找回密码</h2>
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
                <Form.Item
                    name="newPassword"
                    rules={[
                        { required: true, message: '请输入新密码' },
                        { min: 6, message: '密码最少6位' },
                        {
                            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/,
                            message: '密码需包含至少1个大写字母、1个小写字母、1个数字和1个特殊字符',
                        },
                    ]}
                >
                    <Input.Password placeholder="请输入新密码"/>
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
                <div className='verificationArea'>
                    <Form.Item
                        name="verificationCode"
                        className='verificationCode'
                        rules={[{ required: true, message: '请输入验证码' }]}
                    >
                        <Input placeholder="请输入验证码"/>
                    </Form.Item>
                    <Form.Item>
                        <VerificationCodeButton 
                            isCodeButtonDisabled={isCodeButtonDisabled}
                            setIsCodeButtonDisabled={setIsCodeButtonDisabled}
                        />
                    </Form.Item>
                </div>
                <Form.Item>
                    <Button type="primary" htmlType="submit" className='submitButton'>
                        确定
                    </Button>
                </Form.Item>
                <div className='toRouter'>
                    <Link to="/">立即登录</Link>
                    <span>没有账号?<Link to="/register">快速注册</Link></span>
                </div>
            </Form>
        </div>
    );
};

export default ForgetPassword;
