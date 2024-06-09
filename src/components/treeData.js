export const treeData = [
    {
        name: 'Professor B',
        attributes: {
            department: 'Computer Science',
            link: 'https://scholar.google.com/b'
        },
        children: [
            {
                name: 'Professor A',
                attributes: {
                    department: 'Computer Science',
                    link: 'https://scholar.google.com/a'
                },
                children: [
                    {
                        name: 'Student A1',
                        attributes: {
                            department: 'Computer Science',
                            link: 'https://linkedin.com/in/studenta1'
                        }
                    },
                    {
                        name: 'Student A2',
                        attributes: {
                            // attributes if any
                        }
                    },
                    {
                        name: 'Student A3',
                        attributes: {
                            // attributes if any
                        }
                    },
                ],
            }
        ],
    }
];
