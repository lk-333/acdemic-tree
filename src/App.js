import React from 'react';
import './App.css';  // 引入 CSS 样式文件

// 定义树形数据结构
const treeData = {
  name: "Harold William Woolhouse",
  university: "University of Adelaide",
  children: [
    {
      name: "Stephen P Long",
      university: "UIUC",
      children: [
        {
          name: "Carl J. Bernacchi",
          university: "UIUC",
          children: []
        },
        {
          name: "Elizabeth A. Ainsworth",
          university: "UIUC",
          children: []
        }
      ]
    }
  ]
};

// 树节点组件
const TreeNode = ({ data }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const toggleOpen = () => setIsOpen(!isOpen);

  return (
    <div className="node">
      <div className="node-content" onClick={toggleOpen}>
        {data.name} ({data.university}) {isOpen ? '-' : '+'}
      </div>
      {isOpen && (
        <div className="children">
          {data.children.map((child, index) => (
            <TreeNode key={index} data={child} />
          ))}
        </div>
      )}
    </div>
  );
};

// 主应用组件
const App = () => {
  return (
    <div className="tree">
      <TreeNode data={treeData} />
    </div>
  );
}

export default App;
