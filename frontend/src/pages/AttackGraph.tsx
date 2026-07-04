import { useCallback, useEffect } from 'react';
import axios from 'axios';
import ReactFlow, { Background, Controls, addEdge, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';

export default function AttackGraph() {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        axios.get('http://localhost:8080/api/scenarios/graph')
            .then(res => {
                setNodes(res.data.nodes || []);
                setEdges(res.data.edges || []);
            })
            .catch(err => console.error("Failed to fetch attack graph", err));
    }, [setNodes, setEdges]);

    const onConnect = useCallback((params: any) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#fff' } }, eds)), [setEdges]);

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold">Attack Graph Visualizer</h2>
                <button className="btn-primary bg-primary hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg">Run Scenario Simulation</button>
            </div>

            <p className="text-gray-400">Map out node transitions across the network visually using drag and drop tools.</p>

            <div className="h-[600px] border border-white/10 rounded-xl overflow-hidden bg-cyber-card relative">
                {nodes.length === 0 && (
                    <div className="absolute inset-0 flex items-center justify-center text-gray-500 pointer-events-none z-10">
                        No nodes or edges available in current graph layer.
                    </div>
                )}
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    fitView
                >
                    <Background color="#fff" gap={16} />
                    <Controls className="bg-black text-black" />
                </ReactFlow>
            </div>
        </div>
    );
}
