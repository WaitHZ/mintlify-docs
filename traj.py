import argparse
from ast import arguments, literal_eval
import os
from tqdm import tqdm
import json
import re


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
                                            else:
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                dst.write(f"🛠`{msg_tool_call['function']['name']}`\n\n")
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
                                        with open("_tmp.json", "w", encoding="utf-8") as f:
                                            print(msg['content'], file=f)
                                        tool_res = json.load(open("_tmp.json", "r", encoding="utf-8"))
                                        tool_res = tool_res["text"]
                                    except:
                                        tool_res = msg['content']
                                    # INSERT_YOUR_CODE
                                    # markdown或html本身并不直接支持用反斜杠等方式转义括号（如 \( 或 \[），
                                    # 但在markdown中反斜杠可用于部分符号的转义，html中可用实体编码。
                                    # 但对于括号 () [] {}，markdown只对部分符号（如\* \_ \#）有特殊转义效果，
                                    # 对括号的反斜杠转义通常不会影响渲染，html也不会特殊处理。
                                    # 所以即使加了反斜杠，渲染时括号依然会显示为括号。
                                    # 如果只是为了在源码中标记未闭合括号，可以加反斜杠，但这不会影响markdown/html的显示。
                                    # 下面代码保留反斜杠转义逻辑，但请注意渲染效果不会有区别。

                                    def escape_unclosed_brackets_with_backslash(s):
                                        pairs = {'(': ')', '[': ']', '{': '}'}
                                        lefts = set(pairs.keys())
                                        rights = set(pairs.values())
                                        stack = []
                                        result = []
                                        for i, c in enumerate(s):
                                            if c in lefts:
                                                stack.append((c, len(result)))
                                                result.append(c)
                                            elif c in rights:
                                                if stack and pairs[stack[-1][0]] == c:
                                                    stack.pop()
                                                    result.append(c)
                                                else:
                                                    result.append(c)
                                            else:
                                                result.append(c)
                                        for left, idx in stack:
                                            result[idx] = '\\' + left
                                        return ''.join(result)

                                    if isinstance(tool_res, str):
                                        tool_res = escape_unclosed_brackets_with_backslash(tool_res)



                                    dst.write(f"<div className=\"result-box\">\n")
                                    dst.write(f"🔍`tool result`\n\n{tool_res}\n\n</div>\n\n")
                                else:
                                    raise NotImplementedError("tool result doesn't have content")
                                    # dst.write(f"<div className=\"result-box\">\n")
                                    # dst.write("🔍`tool result`\n```json\n{}\n```\n</div>\n\n")
                            else:
                                raise NotImplementedError(f"Unsupported message role: {msg['role']}")

                        dst.write(f"</Accordion>\n\n")
            
            if len(os.listdir(log_dir)) > 0:
                dst.write(f"</AccordionGroup>\n")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_dir", type=str, default="docs/tasks")
    args = parser.parse_args()
    main(args)