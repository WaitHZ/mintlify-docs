import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  const { taskId } = req.query;

  try {
    // 构建轨迹文件路径
    const trajDir = path.join(process.cwd(), 'traj', taskId);
    
    // 检查目录是否存在
    if (!fs.existsSync(trajDir)) {
      return res.status(404).json({ error: 'Task not found' });
    }

    // 读取目录中的所有 JSON 文件
    const files = fs.readdirSync(trajDir).filter(file => file.endsWith('.json'));
    
    if (files.length === 0) {
      return res.status(404).json({ error: 'No trajectory files found' });
    }

    // 解析所有轨迹文件
    const trajectories = files.map(file => {
      const filePath = path.join(trajDir, file);
      const fileContent = fs.readFileSync(filePath, 'utf8');
      const trajectoryData = JSON.parse(fileContent);
      
      // 解析消息并构建轮次
      const turns = parseMessages(trajectoryData.messages);
      
      return {
        id: file.replace('.json', ''),
        model: extractModelName(file),
        date: trajectoryData.initial_run_time?.split(' ')[0] || 'Unknown',
        status: trajectoryData.status || 'unknown',
        duration: calculateDuration(trajectoryData.initial_run_time, trajectoryData.completion_time),
        messages: trajectoryData.messages?.length || 0,
        turns: turns,
        metrics: {
          totalTokens: trajectoryData.key_stats?.total_tokens || 0,
          inputTokens: trajectoryData.key_stats?.input_tokens || 0,
          outputTokens: trajectoryData.key_stats?.output_tokens || 0,
          cost: trajectoryData.agent_cost?.total_cost || 0,
          toolCalls: trajectoryData.key_stats?.tool_calls || 0
        }
      };
    });

    res.status(200).json(trajectories);
  } catch (error) {
    console.error('Error reading trajectory files:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

function parseMessages(messages) {
  if (!messages || !Array.isArray(messages)) {
    return [];
  }

  const turns = [];
  let currentTurn = null;

  messages.forEach((message, index) => {
    if (message.role === 'user') {
      // 开始新的轮次
      if (currentTurn) {
        turns.push(currentTurn);
      }
      currentTurn = {
        type: 'user',
        content: message.content,
        toolCalls: []
      };
    } else if (message.role === 'assistant') {
      if (!currentTurn) {
        currentTurn = {
          type: 'agent',
          content: message.content || '',
          toolCalls: []
        };
      } else {
        currentTurn.type = 'agent';
        currentTurn.content = message.content || '';
      }

      // 处理工具调用
      if (message.tool_calls && Array.isArray(message.tool_calls)) {
        message.tool_calls.forEach(toolCall => {
          currentTurn.toolCalls.push({
            id: toolCall.id,
            name: toolCall.function?.name || 'unknown',
            parameters: toolCall.function?.arguments || '{}',
            response: null // 工具响应在下一个消息中
          });
        });
      }
    } else if (message.role === 'tool') {
      // 工具响应
      if (currentTurn && currentTurn.toolCalls.length > 0) {
        const lastToolCall = currentTurn.toolCalls[currentTurn.toolCalls.length - 1];
        if (lastToolCall && !lastToolCall.response) {
          lastToolCall.response = message.content;
        }
      }
    }
  });

  // 添加最后一个轮次
  if (currentTurn) {
    turns.push(currentTurn);
  }

  return turns;
}

function extractModelName(filename) {
  // 从文件名中提取模型名称
  // 例如: claude-4-sonnet-0514.json -> Claude 4 Sonnet
  const parts = filename.replace('.json', '').split('-');
  if (parts[0] === 'claude') {
    return `Claude ${parts[1]} ${parts[2]}`;
  } else if (parts[0] === 'gpt') {
    return `GPT-${parts[1]}`;
  } else if (parts[0] === 'gemini') {
    return `Gemini ${parts[1]}`;
  }
  return filename.replace('.json', '');
}

function calculateDuration(startTime, endTime) {
  if (!startTime || !endTime) {
    return 'Unknown';
  }

  try {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diffMs = end - start;
    const diffSeconds = Math.floor(diffMs / 1000);
    
    if (diffSeconds < 60) {
      return `${diffSeconds}s`;
    } else {
      const minutes = Math.floor(diffSeconds / 60);
      const seconds = diffSeconds % 60;
      return `${minutes}m ${seconds}s`;
    }
  } catch (error) {
    return 'Unknown';
  }
}
