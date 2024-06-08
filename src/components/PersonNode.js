import React from 'react';

const PersonNode = ({ person }) => {
    const handleClick = () => {
        // 点击事件逻辑，例如跳转到LinkedIn或Google Scholar
        window.open(person.profileLink, '_blank');
    };

    return (
        <div className="person-node" onClick={handleClick}>
            <h3>{person.name}</h3>
            <p>{person.title}</p>
        </div>
    );
};

export default PersonNode;
