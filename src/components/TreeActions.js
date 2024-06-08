import React from 'react';

const TreeActions = ({ onAdd, onEdit, onDelete }) => {
    return (
        <div className="tree-actions">
            <button onClick={onAdd}>添加节点</button>
            <button onClick={onEdit}>编辑节点</button>
            <button onClick={onDelete}>删除节点</button>
        </div>
    );
};

export default TreeActions;
