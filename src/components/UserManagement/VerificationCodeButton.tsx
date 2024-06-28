import React, { useState,useEffect } from 'react';
import {  Button, Form } from 'antd';

export default function  VerificationCodeButton ({ isCodeButtonDisabled, setIsCodeButtonDisabled }) {
    const [count, setCount] = useState(0); // 初始计时为0
    const [haveSend, setHaveSend] = useState(false);
    if(count>0)
    {
        setIsCodeButtonDisabled(true)
    }

    const handleSendCode = () => {
        // 假设发送验证码操作成功后开始倒计时
        setCount(60); // 设置倒计时的时间，例如60秒
        setHaveSend(true)
    };

    useEffect(() => {
        // 每当count变化时设置一个定时器
        if (count > 0) {
            const timer = setTimeout(() => {
                setCount(count - 1); // 每秒减少1
            }, 1000);
            return () => clearTimeout(timer); // 清除定时器
        }
    }, [count]);

    let content;
    if(isCodeButtonDisabled && haveSend)
    {
        content=count+"秒后重新发送"
    }
    else
    {
        content="发送验证码"
    }
    return (
        <Form.Item>
            <Button 
                type="primary" 
                className='verificationCode_button' 
                onClick={handleSendCode} 
                disabled={isCodeButtonDisabled}
            >
                
                {content}
            </Button>
        </Form.Item>
    );
};