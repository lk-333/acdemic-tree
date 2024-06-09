import React from 'react';
import Tree from 'react-d3-tree';
import './MyTreeComponent.css'; // 确保你有适当的CSS样式
import { treeData } from './treeData';

const MyTreeComponent = () => {
    const handleNodeClick = (nodeData) => {
        if (nodeData.attributes && nodeData.attributes.link) {
            window.open(nodeData.attributes.link, "_blank");
        }
    };

    return (
        <div id="treeWrapper" style={{ width: '100%', height: '500px' }}>
            <Tree
                data={treeData}
                orientation="vertical"
                translate={{ x: 250, y: 250 }}
                onNodeClick={handleNodeClick}
                pathFunc="elbow"
            />
        </div>
    );
};

export default MyTreeComponent;
