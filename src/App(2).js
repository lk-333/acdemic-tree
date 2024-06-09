// App.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';


const App = () => {
     const navigate = useNavigate();

    const handleCreateTreeClick = () => {
        navigate('/create-tree');
    };

    const handleSearchTreeClick = () => {
        navigate('/search-tree');
    };

   return (
        <div>
            <h1>主页面</h1>
            <button onClick={handleCreateTreeClick} className="margin-right">创建师承树</button>
            <button onClick={handleSearchTreeClick}>查询师承树</button>
        </div>
    );

};

export default App;
