import argparse
from ast import arguments, literal_eval
import os
from tqdm import tqdm
import json
import re


icon_map = {
    "arxiv_local": '<svg width="14" height="14" viewBox="0 0 17.732 24.269" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#bdb9b4" d="m6.565 9.368 2.266 2.738 6.674-7.84c.353-.47.52-.717.353-1.117a1.218 1.218 0 0 0-1.061-.748.953.953 0 0 0-.712.262Z"/><path fill="#b31b1b" d="M12.541 10.677 1.935.503a1.413 1.413 0 0 0-.834-.5 1.09 1.09 0 0 0-1.027.66c-.167.4-.047.681.319 1.206l8.44 10.242-6.282 7.716a1.336 1.336 0 0 0-.323 1.3 1.114 1.114 0 0 0 1.04.69.992.992 0 0 0 .748-.365l8.519-7.92a1.924 1.924 0 0 0 .006-2.855Z"/><path fill="#bdb9b4" d="M17.336 22.364 8.811 12.089 6.546 9.352l-1.389 1.254a2.063 2.063 0 0 0 0 2.965L15.969 23.99a.925.925 0 0 0 .742.282 1.039 1.039 0 0 0 .953-.667 1.261 1.261 0 0 0-.328-1.241Z"/></svg>',
    "filesystem": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#FFA000" d="M40,12H22l-4-4H8c-2.2,0-4,1.8-4,4v8h40v-4C44,13.8,42.2,12,40,12z"/><path fill="#FFCA28" d="M40,12H8c-2.2,0-4,1.8-4,4v20c0,2.2,1.8,4,4,4h32c2.2,0,4-1.8,4-4V16C44,13.8,42.2,12,40,12z"/></svg>'
}


def find_mdx_files_with_underscore(dir_path):
    mdx_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith("_.mdx"):
                mdx_files.append(os.path.join(root, file))
    return mdx_files


def clear(task_dir):
    for root, dirs, files in os.walk(task_dir):
        for file in files:
            if file.endswith("__.mdx"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")


def raw_json_str_to_python(obj: str) -> dict:
    """
    把控制台里打印出来的“伪 JSON 字符串”还原成 Python 对象。
    1. 去掉首尾的引号（如果有）
    2. 把真正的 JSON 需要的转义补回去
    3. json.loads 解析
    """
    # 1. 去掉首尾可能被人手工包上的双引号
    obj = obj.strip()
    if (obj.startswith('"') and obj.endswith('"')) or \
       (obj.startswith("'") and obj.endswith("'")):
        obj = obj[1:-1]

    # 2. 把“用户眼里”的反斜杠变成“JSON 眼里”的反斜杠
    #    即：\n  -> \\n
    #        \" -> \\\"
    #        \\ -> \\\\
    obj = obj.encode('utf-8').decode('unicode_escape')   # 先解开 \n \t \"
    obj = obj.replace('\\', r'\\')                       # 再整体把反斜杠翻倍
    obj = obj.replace(r'\"', r'\"')                      # 把已经翻倍的 \" 还原

    # 3. 现在它是合法 JSON 字符串了
    return json.loads(obj)


def main(args):

    task_dir = args.task_dir

    clear(task_dir)

    mdx_files = find_mdx_files_with_underscore(task_dir)
    for f in tqdm(mdx_files):
        f_prefix = f.replace("_.mdx", "")
        print(f_prefix)
        target_md = f_prefix + ".mdx"
        print(target_md)

        with open(f, "r", encoding="utf-8") as src, open(target_md, "w", encoding="utf-8") as dst:
            dst.write(src.read())

            log_dir = f_prefix + "/"

            if len(os.listdir(log_dir)) > 0:
                dst.write(f"\n<AccordionGroup>\n")

            for log_file in sorted(os.listdir(log_dir)):
                if log_file.endswith(".json"):
                    log_path = os.path.join(log_dir, log_file)
                    with open(log_path, "r", encoding="utf-8") as lf:
                        log_data = json.load(lf)
                        msgs = log_data["messages"]
                        
                        model_name = log_path.split("/")[-1].replace(".json", "")
                        dst.write(f"<Accordion title=\"{model_name}\">\n\n")

                        dst.write("<Columns cols={3}>\n")
                        if log_data["pass"]:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"check\">\n")
                            dst.write(f"Completed\n")
                        else:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"x\">\n")
                            dst.write(f"Failed\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Tool Calls\" icon=\"wrench\">\n")
                        tool_call_num = 0
                        for msg in msgs:
                            if msg["role"] == "assistant" and "tool_calls" in msg:
                                tool_call_num += len(msg["tool_calls"])
                        dst.write(f"{tool_call_num}\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Turns\" icon=\"arrows-rotate\">\n")
                        assit_msgs = [msg for msg in msgs if msg["role"] == "assistant"]
                        dst.write(f"{len(assit_msgs)}\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"</Columns>\n\n")

                        for msg in msgs:
                            if msg["role"] == "user":
                                continue
                            elif msg["role"] == "assistant":
                                if "tool_calls" in msg:
                                    if not (msg["content"] == "" or msg["content"] is None or msg["content"] == "null"):
                                        dst.write(f"<div className=\"thinking-box\">\n")
                                        dst.write(f"🧐`Agent`\n\n{msg['content'].strip()}\n</div>\n\n")

                                    for msg_tool_call in msg["tool_calls"]:
                                        if msg_tool_call['type'] == "function":
                                            if msg_tool_call['function']['name'] == "local-python-execute":
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                dst.write(f"🛠`{msg_tool_call['function']['name']}`\n\n")
                                                arg_s = json.loads(msg_tool_call['function']['arguments'])
                                                dst.write(f"```python {arg_s['filename'] if 'filename' in arg_s else ''}\n")
                                                dst.write(f"{arg_s['code']}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                            elif msg_tool_call['function']['name'] == "filesystem-write_file":
                                                arg_s = json.loads(msg_tool_call['function']['arguments'])
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                dst.write(f"{icon_map['filesystem']}`{msg_tool_call['function']['name']}`\n\n")
                                                dst.write(f"```text workspace/{arg_s['path'].split('/')[-1]}\n")
                                                dst.write(f"{arg_s['content']}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                            else:
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                server_name = msg_tool_call['function']['name'].split('-')[0] if "-" in msg_tool_call['function']['name'] else msg_tool_call['function']['name']
                                                dst.write(icon_map[server_name] if server_name in icon_map else "🛠")
                                                dst.write(f"`{msg_tool_call['function']['name'].replace('-', ' ')}`\n\n")
                                                dst.write(f"```json\n")
                                                argu_s = msg_tool_call['function']['arguments'].strip()[1:-1].split(",")
                                                if len(argu_s) == 1 and argu_s[0] == "":
                                                    dst.write("{}\n")
                                                else:
                                                    dst.write("{\n")
                                                    for i, arg in enumerate(argu_s):
                                                        if i == 0:
                                                            dst.write(f"\t{arg}")
                                                        else:
                                                            dst.write(f",\n\t{arg}")
                                                    dst.write("\n}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                        else:
                                            raise NotImplementedError(f"Unsupported tool call type: {msg_tool_call['type']}")
                                else:
                                    dst.write(f"<div className=\"thinking-box\">\n")
                                    dst.write(f"🧐`Agent`\n\n{msg['content'].strip()}\n</div>\n\n")
                            elif msg["role"] == "tool":
                                if msg['content'] is not None:
                                    try:
                                        # tool_res.replace(r'\"', r'"')
                                        # tool_res.replace(r'\\n', r'\n')
                                        with open("_tmp", "w", encoding="utf-8") as f:
                                            print(msg['content'], file=f)
                                        tool_res = json.load(open("_tmp", "r", encoding="utf-8"))
                                        tool_res = tool_res["text"]
                                        tool_res = tool_res.replace('```', '')
                                    except:
                                        tool_res = msg['content']
                                        if tool_res.startswith('[') and tool_res.endswith(']'):
                                            tool_res = tool_res.replace('[{', '[\n{')
                                            tool_res = tool_res.replace('}]', '}\n]')
                                            tool_res = tool_res.replace('}, {', '},\n{')
                                            tool_res = tool_res.replace(r'\n', ' ')

                                    dst.write(f"<div className=\"result-box\">\n")
                                    dst.write(f"🔍`tool result`\n```json\n{tool_res}\n```\n</div>\n\n")
                                else:
                                    raise NotImplementedError("tool result doesn't have content")
                                    # dst.write(f"<div className=\"result-box\">\n")
                                    # dst.write("🔍`tool result`\n```json\n{}\n```\n</div>\n\n")
                            else:
                                raise NotImplementedError(f"Unsupported message role: {msg['role']}")

                        dst.write(f"</Accordion>\n\n")
            
            if len(os.listdir(log_dir)) > 0:
                dst.write(f"</AccordionGroup>\n")

    _tmp_path = os.path.join(os.path.dirname(__file__), "_tmp")
    try:
        os.remove(_tmp_path)
    except FileNotFoundError:
        print(f"File {_tmp_path} not found, don't need to remove")
    else:
        print(f"Removed file {_tmp_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_dir", type=str, default="docs/tasks")
    args = parser.parse_args()
    main(args)