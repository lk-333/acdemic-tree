import React, { useEffect, useRef } from 'react';import * as d3 from './customD3'; // 导入自定义的 d3 模块
import './MyTreeComponent.css'; // 引入 CSS 文件
import { useLocation } from 'react-router-dom';

const AcademicTree = () => {
    const svgRef = useRef();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const id = queryParams.get('id');

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/bulid_tree',{
                method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id })
            });
            const data = await response.json();
            const width = 1000;
            const height = 600;
            d3.select(svgRef.current).selectAll('*').remove();

            const svg = d3.select(svgRef.current)
                .attr('width', width)
                .attr('height', height);

            svg.append('g')
                .selectAll('line')
                .data(data.links)
                .enter().append('line')
                .attr('stroke', '#999')
                .attr('stroke-width', 2)
                .attr('x1', d => data.nodes.find(node => node.real_name === d.source).x)
                .attr('y1', d => data.nodes.find(node => node.real_name === d.source).y)
                .attr('x2', d => data.nodes.find(node => node.real_name === d.target).x)
                .attr('y2', d => data.nodes.find(node => node.real_name === d.target).y);

            svg.append('g')
                .selectAll('circle')
                .data(data.nodes)
                .enter().append('circle')
                .attr('r', 10)
                .attr('fill', '#69b3a2')
                .attr('cx', d => d.x)
                .attr('cy', d => d.y)
                .on('click', (event, d) => {
                    if (d.profile_link) {
                        window.open(d.profile_link, '_blank');
                    } else {
                        alert(`Node: ${d.real_name}`);
                        // 发送一个新的请求给后端（id）
                        // 后端发送一个新的树
                        // 前端渲染


                    }
                });

            svg.append('g')
                .selectAll('text')
                .data(data.nodes)
                .enter().append('text')
                .attr('dy', -10)
                .attr('text-anchor', 'middle')
                .attr('x', d => d.x)
                .attr('y', d => d.y)
                .text(d => d.real_name);
        };

        fetchData();
    }, []);

    return (
        <div className="svg-container">
            <svg ref={svgRef}></svg>
        </div>
    );
};

export default AcademicTree;
