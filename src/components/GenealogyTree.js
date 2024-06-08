import React from 'react';
import PersonNode from './PersonNode';

const GenealogyTree = ({ treeData }) => {
    return (
        <div className="genealogy-tree">
            {treeData.map((person) => (
                <PersonNode key={person.id} person={person} />
            ))}
        </div>
    );
};

export default GenealogyTree;
