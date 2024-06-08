import React, { useState } from 'react';

const AddEditNodeForm = ({ onSave, initialData }) => {
    const [person, setPerson] = useState(initialData || {
        name: '',
        title: '',
        profileLink: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPerson((prevPerson) => ({ ...prevPerson, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(person);
    };

    return (
        <form className="add-edit-node-form" onSubmit={handleSubmit}>
            <input
                type="text"
                name="name"
                value={person.name}
                onChange={handleChange}
                placeholder="姓名"
            />
            <input
                type="text"
                name="title"
                value={person.title}
                onChange={handleChange}
                placeholder="职称"
            />
            <input
                type="text"
                name="profileLink"
                value={person.profileLink}
                onChange={handleChange}
                placeholder="LinkedIn或Google Scholar链接"
            />
            <button type="submit">保存</button>
        </form>
    );
};

export default AddEditNodeForm;
