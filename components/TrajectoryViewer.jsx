import React, { useState, useEffect } from 'react';

const TrajectoryViewer = ({ taskId }) => {
  const [trajectories, setTrajectories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadTrajectories = async () => {
      try {
        setLoading(true);
        // 这里需要根据实际的 API 或文件系统来读取轨迹数据
        // 暂时使用模拟数据，实际实现时需要替换为真实的 API 调用
        const response = await fetch(`/api/trajectories/${taskId}`);
        if (!response.ok) {
          throw new Error('Failed to load trajectories');
        }
        const data = await response.json();
        setTrajectories(data);
      } catch (err) {
        setError(err.message);
        // 如果 API 不可用，使用本地数据
        setTrajectories([{
          id: 'claude-4-sonnet-0514',
          model: 'Claude 4 Sonnet',
          date: '2025-07-14',
          status: 'success',
          duration: '54s',
          messages: 25,
          turns: [
            {
              type: 'user',
              content: "I'm looking for a paper on arxiv related to agentic reasoning. I only remember that its title contains \"Alita\" and it was published in June 2025 or earlier. Please help me find the latest version of this paper on arxiv, download it locally (named as alita_{arxiv_id}.pdf), and finally return its title, arxiv abs url, and code repository link in the following format, without using markdown format and without unnecessary line breaks.\n\ntitle: {title}\narxiv_abs_url: {arxiv_abs_url}\ncode_url: {code_url}"
            },
            {
              type: 'agent',
              content: "I'll help you find the paper related to \"Alita\" and agentic reasoning on arXiv. Let me search for it first.",
              toolCalls: [
                {
                  name: 'arxiv_local-search_papers',
                  parameters: '{"date_to":"2025-06-30","max_results":10,"query":"Alita agentic reasoning"}',
                  response: '{"total_results": 0, "papers": []}'
                }
              ]
            }
            // 更多轮次...
          ]
        }]);
      } finally {
        setLoading(false);
      }
    };

    loadTrajectories();
  }, [taskId]);

  if (loading) {
    return <div>Loading trajectories...</div>;
  }

  if (error) {
    return <div>Error loading trajectories: {error}</div>;
  }

  return (
    <div className="trajectory-viewer">
      {trajectories.map((traj) => (
        <div key={traj.id} className="trajectory-item">
          <h3>{traj.model} (Run: {traj.date})</h3>
          <div className="trajectory-stats">
            <span>Status: {traj.status}</span>
            <span>Duration: {traj.duration}</span>
            <span>Messages: {traj.messages}</span>
          </div>
          <div className="trajectory-turns">
            {traj.turns.map((turn, index) => (
              <div key={index} className={`turn turn-${turn.type}`}>
                <h4>Turn {index + 1}: {turn.type === 'user' ? 'User Request' : 'Agent Response'}</h4>
                <div className="turn-content">
                  <strong>{turn.type === 'user' ? 'User' : 'Agent'}:</strong>
                  <pre>{turn.content}</pre>
                  {turn.toolCalls && (
                    <div className="tool-calls">
                      {turn.toolCalls.map((tool, toolIndex) => (
                        <div key={toolIndex} className="tool-call">
                          <strong>Tool Call:</strong> <code>{tool.name}</code>
                          <br />
                          <strong>Parameters:</strong> <code>{tool.parameters}</code>
                          <br />
                          <strong>Response:</strong> <code>{tool.response}</code>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TrajectoryViewer;
