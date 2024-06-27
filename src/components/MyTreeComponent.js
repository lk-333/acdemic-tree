import React, { useEffect, useRef } from 'react';
import * as d3 from './customD3'; // 导入自定义的 d3 模块
import './MyTreeComponent.css'; // 引入 CSS 文件
import { useLocation,useNavigate  } from 'react-router-dom';

const AcademicTree = () => {
    const svgRef = useRef();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const id = queryParams.get('id');
    const navigate = useNavigate();

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
                .attr('height', height)
                .attr('viewBox', `0 0 ${width} ${height}`)
                .style('border', '1px solid black');

            // 绘制可视连线
            const links = svg.append('g')
                .selectAll('line')
                .data(data.links)
                .enter().append('line')
                .attr('stroke', '#999')
                .attr('stroke-width', 2)
                .attr('x1', d => data.nodes.find(node => node.real_name === d.source).x)
                .attr('y1', d => data.nodes.find(node => node.real_name === d.source).y + 10)
                .attr('x2', d => data.nodes.find(node => node.real_name === d.target).x)
                .attr('y2', d => data.nodes.find(node => node.real_name === d.target).y - 10);

            // 绘制透明的交互线条
            svg.append('g')
                .selectAll('line.interactive')
                .data(data.links)
                .enter().append('line')
                .classed('interactive', true)
                .attr('stroke', 'transparent')
                .attr('stroke-width', 10) // 宽度足够大以便于交互
                .attr('x1', d => data.nodes.find(node => node.real_name === d.source).x)
                .attr('y1', d => data.nodes.find(node => node.real_name === d.source).y + 10)
                .attr('x2', d => data.nodes.find(node => node.real_name === d.target).x)
                .attr('y2', d => data.nodes.find(node => node.real_name === d.target).y - 10)
                .on('mouseenter', function (event, d) {
                    const x = (data.nodes.find(node => node.real_name === d.source).x + data.nodes.find(node => node.real_name === d.target).x) / 2;
                    const y = (data.nodes.find(node => node.real_name === d.source).y + data.nodes.find(node => node.real_name === d.target).y) / 2;

                    svg.append('text')
                        .attr('x', x)
                        .attr('y', y)
                        .attr('text-anchor', 'middle')
                        .attr('real_name', 'hoverText')
                        .text('2018-2022');
                })
                .on('mouseleave', function () {
                    d3.select('#hoverText').remove(); // 移除 hover 文本
                });

            // 绘制节点文本
            svg.append('g')
                .selectAll('text')
                .data(data.nodes)
                .enter().append('text')
                .attr('dy', 3) // 调整文字位置
                .attr('text-anchor', 'middle')
                .attr('x', d => d.x)
                .attr('y', d => d.y)
                .attr('font-size', 16)
                .attr('fill', '#333')
                .attr('font-weight', d => d.profile_link ? 'bold' : 'normal') // 加粗有 profile_link 的节点
                .style('cursor', 'default')  // 设置鼠标样式
                .text(d => d.real_name)
                .on('click', (event, d) => {
                    if (d.profile_link) {
                        window.open(d.profile_link, '_blank');
                    } else {
                        navigate(`/create-tree?id=222`);
                    }
                });

            // 添加鼠标悬停事件来显示文本
            links.on('mouseenter', function (event, d) {
                const x = (data.nodes.find(node => node.real_name === d.source).x + data.nodes.find(node => node.real_name === d.target).x) / 2;
                const y = (data.nodes.find(node => node.real_name === d.source).y + data.nodes.find(node => node.real_name === d.target).y) / 2;

                svg.append('text')
                    .attr('x', x)
                    .attr('y', y)
                    .attr('text-anchor', 'middle')
                    .attr('real_name', 'hoverText')
                    .text('2018-2022');
            })
            .on('mouseleave', function () {
                d3.select('#hoverText').remove(); // 移除 hover 文本
            });

        };

        fetchData();
    },[])

    return (
        <div className="svg-container" style={{ position: 'relative' }}>
            <svg ref={svgRef}></svg>
        </div>
    );
};

export default AcademicTree;
