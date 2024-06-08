import React, { useState } from 'react';
import GenealogyTree from './components/GenealogyTree';
import SearchBar from './components/SearchBar';
import AddEditNodeForm from './components/AddEditNodeForm';
import TreeActions from './components/TreeActions';
import './styles.css';

const App = () => {
    const [treeData, setTreeData] = useState([]);
    const [selectedNode, setSelectedNode] = useState(null);

    const handleSearch = (query) => {
        // 查询逻辑
        // 示例：在 treeData 中查找名字匹配 query 的节点
        const result = treeData.find(person => person.name.includes(query));
        if (result) {
            // 设置选中的节点
            setSelectedNode(result);
        } else {
            // 处理未找到结果的情况
            alert('未找到相关人员');
        }
    };

    const handleAddNode = () => {
        // 添加节点逻辑
        const newNode = {
            id: treeData.length + 1,
            name: '新节点',
            title: '职称',
            profileLink: ''
        };
        setTreeData([...treeData, newNode]);
    };

    const handleEditNode = () => {
        // 编辑节点逻辑
        if (selectedNode) {
            setTreeData(treeData.map(node => node.id === selectedNode.id ? selectedNode : node));
            setSelectedNode(null);
        }
    };

    const handleDeleteNode = () => {
        // 删除节点逻辑
        if (selectedNode) {
            setTreeData(treeData.filter(node => node.id !== selectedNode.id));
            setSelectedNode(null);
        }
    };

    const handleSaveNode = (node) => {
        // 保存节点逻辑
        if (selectedNode) {
            setTreeData(treeData.map(n => n.id === selectedNode.id ? node : n));
        } else {
            setTreeData([...treeData, node]);
        }
        setSelectedNode(null);
    };

    return (
        <div className="app">
            <SearchBar onSearch={handleSearch} />
            <TreeActions onAdd={handleAddNode} onEdit={handleEditNode} onDelete={handleDeleteNode} />
            <GenealogyTree treeData={treeData} />
            {selectedNode && (
                <AddEditNodeForm onSave={handleSaveNode} initialData={selectedNode} />
            )}
        </div>
    );
};

export default App;
