import json
import os
from pathlib import Path
import argparse
from tqdm import tqdm

def process_task(task_dir):
    """Process a single task directory"""
    task_name = task_dir.name
    log_file = task_dir / "log.json"
    
    if not log_file.exists():
        print(f"Warning: {log_file} does not exist")
        return
    
    # Read log file
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract messages
    messages = data.get('messages', [])
    if not messages:
        print(f"Warning: No messages found in {log_file}")
        return
    
    # Generate MDX content
    mdx_path = task_dir.parent / f"{task_name}.mdx"
    print(f"Writing to: {mdx_path}")
    
    with open(mdx_path, 'w', encoding='utf-8') as dst:
        # Write frontmatter
        dst.write(f"---\n")
        dst.write(f"title: \"{task_name}\"\n")
        dst.write(f"---\n\n")
        
        # Write accordion group
        dst.write(f"<AccordionGroup>\n")
        
        # Get model name from data
        model_name = data.get('model_name', 'unknown-model')
        dst.write(f"<Accordion title=\"{model_name}\">\n\n")
        
        # Write stats cards
        dst.write(f"<Columns cols={{2}}>\n")
        dst.write(f"<Card title=\"Task Completion\" icon=\"check\">\n")
        
        # Determine completion status
        task_pass = data.get('pass', False)
        completion_status = "Completed" if task_pass else "Failed"
        dst.write(f"{completion_status}\n")
        dst.write(f"</Card>\n")
        
        # Count tool calls
        tool_call_count = 0
        for msg in messages:
            if msg.get('role') == 'assistant' and msg.get('tool_calls'):
                tool_call_count += len(msg['tool_calls'])
        
        dst.write(f"<Card title=\"Tool Calls\" icon=\"wrench\">\n")
        dst.write(f"{tool_call_count}\n")
        dst.write(f"</Card>\n")
        dst.write(f"</Columns>\n\n")
        
        # Process messages
        for msg in messages:
            if msg["role"] == "user":
                dst.write(f"<div className=\"thinking-box\">\n")
                dst.write(f"🧐{msg['content']}\n")
                dst.write(f"</div>\n\n")
            elif msg["role"] == "assistant":
                if msg.get("tool_calls"):
                    for msg_tool_call in msg["tool_calls"]:
                        if msg_tool_call["type"] == "function":
                            dst.write(f"<div className=\"tool-call-box\">\n")
                            dst.write(f"🛠`{msg_tool_call['function']['name']}`\n\n")
                            dst.write(f"```json\n{msg_tool_call['function']['arguments']}\n```\n")
                            dst.write(f"</div>\n\n")
                        else:
                            raise NotImplementedError(f"Unsupported tool call type: {msg_tool_call['type']}")
                else:
                    if msg.get('content'):
                        dst.write(f"<div className=\"thinking-box\">\n")
                        dst.write(f"🧐{msg['content']}\n</div>\n\n")
                    else:
                        dst.write(f"<div className=\"task-completed-box\">\n")
                        dst.write(f"📢Task completed\n</div>\n\n")
            elif msg["role"] == "tool":
                dst.write(f"<div className=\"result-box\">\n")
                
                # Enhanced error handling for content
                content = msg.get('content')
                if content is not None and content.strip():
                    try:
                        tool_res = json.loads(content)
                        if isinstance(tool_res, dict) and tool_res.get("type") == "text":
                            dst.write(f"🔍\n```json\n{tool_res['text']}\n```\n")
                        else:
                            # If it's not the expected format, just write the content
                            dst.write(f"🔍\n```json\n{content}\n```\n")
                    except json.JSONDecodeError as e:
                        print(f"Warning: JSON decode error for content: {content[:100]}...")
                        print(f"Error: {e}")
                        dst.write(f"🔍\n```text\n{content}\n```\n")
                else:
                    dst.write(f"🔍\n```json\n{{}}\n```\n")
                
                dst.write(f"</div>\n\n")
            else:
                print(f"Warning: Unsupported message role: {msg['role']}")
        
        # Close accordion and group
        dst.write(f"</Accordion>\n")
        dst.write(f"</AccordionGroup>\n")

def main(args):
    """Main function to process all tasks"""
    docs_dir = Path("docs/tasks")
    
    # Find all task directories
    task_dirs = []
    for category_dir in docs_dir.iterdir():
        if category_dir.is_dir():
            for task_dir in category_dir.iterdir():
                if task_dir.is_dir() and (task_dir / "log.json").exists():
                    task_dirs.append(task_dir)
    
    print(f"Found {len(task_dirs)} task directories")
    
    # Process each task
    for task_dir in tqdm(task_dirs):
        print(f"Processing: {task_dir}")
        try:
            process_task(task_dir)
        except Exception as e:
            print(f"Error processing {task_dir}: {e}")
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert task logs to MDX format")
    args = parser.parse_args()
    main(args)