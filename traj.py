import argparse
from ast import arguments, literal_eval
import os
from tqdm import tqdm
import json
import re


icon_map = {
    "arxiv_local": '<svg width="14" height="14" viewBox="0 0 17.732 24.269" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#bdb9b4" d="m6.565 9.368 2.266 2.738 6.674-7.84c.353-.47.52-.717.353-1.117a1.218 1.218 0 0 0-1.061-.748.953.953 0 0 0-.712.262Z"/><path fill="#b31b1b" d="M12.541 10.677 1.935.503a1.413 1.413 0 0 0-.834-.5 1.09 1.09 0 0 0-1.027.66c-.167.4-.047.681.319 1.206l8.44 10.242-6.282 7.716a1.336 1.336 0 0 0-.323 1.3 1.114 1.114 0 0 0 1.04.69.992.992 0 0 0 .748-.365l8.519-7.92a1.924 1.924 0 0 0 .006-2.855Z"/><path fill="#bdb9b4" d="M17.336 22.364 8.811 12.089 6.546 9.352l-1.389 1.254a2.063 2.063 0 0 0 0 2.965L15.969 23.99a.925.925 0 0 0 .742.282 1.039 1.039 0 0 0 .953-.667 1.261 1.261 0 0 0-.328-1.241Z"/></svg>',
    "filesystem": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#FFA000" d="M40,12H22l-4-4H8c-2.2,0-4,1.8-4,4v8h40v-4C44,13.8,42.2,12,40,12z"/><path fill="#FFCA28" d="M40,12H8c-2.2,0-4,1.8-4,4v20c0,2.2,1.8,4,4,4h32c2.2,0,4-1.8,4-4V16C44,13.8,42.2,12,40,12z"/></svg>',
    "scholarly": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#1e88e5" d="M24,4C12.954,4,4,12.954,4,24s8.954,20,20,20s20-8.954,20-20S35.046,4,24,4z"/><path fill="#1565c0" d="M35,16.592v-3.878L37,11H27l0.917,1.833c-1.236,0-2.265,0-2.265,0S19.095,13,19.095,18.748	c0,5.752,5.732,5.088,5.732,5.088s0,0.865,0,1.453c0,0.594,0.77,0.391,0.864,1.583c-0.388,0-7.964-0.208-7.964,4.998	s6.679,4.959,6.679,4.959s7.722,0.365,7.722-6.104c0-3.871-4.405-5.121-4.405-6.686c0-1.563,3.319-2.012,3.319-5.684	c0-0.823-0.028-1.524-0.149-2.12L34,13.571v3.02c-0.581,0.207-1,0.756-1,1.408v4.5c0,0.829,0.672,1.5,1.5,1.5s1.5-0.671,1.5-1.5V18	C36,17.348,35.581,16.799,35,16.592z M30.047,31.169c0.131,2.024-1.929,3.811-4.603,3.998c-2.671,0.188-4.946-1.295-5.077-3.316	c-0.133-2.016,1.927-3.805,4.6-3.996C27.641,27.667,29.914,29.152,30.047,31.169z M26.109,22.453	c-1.592,0.451-3.375-1.062-3.982-3.367c-0.604-2.312,0.195-4.543,1.786-4.992c1.593-0.453,3.374,1.059,3.981,3.367	C28.499,19.77,27.702,22.004,26.109,22.453z"/><path fill="#e8eaf6" d="M34,16.592V12c0-0.051-0.015-0.097-0.029-0.143L35,11H21l-9,8h5.383	c0.174,5.466,5.715,4.836,5.715,4.836s0,0.865,0,1.453c0,0.594,0.771,0.391,0.865,1.583c-0.388,0-7.964-0.208-7.964,4.998	s6.679,4.959,6.679,4.959s7.721,0.365,7.721-6.104c0-3.871-4.404-5.121-4.404-6.686c0-1.563,3.318-2.012,3.318-5.684	c0-0.971-0.047-1.763-0.232-2.422L33,12.667v3.925c-0.581,0.207-1,0.756-1,1.408v4.5c0,0.829,0.672,1.5,1.5,1.5s1.5-0.671,1.5-1.5	V18C35,17.348,34.581,16.799,34,16.592z M28.319,31.169c0.131,2.024-1.928,3.811-4.602,3.998c-2.671,0.188-4.946-1.295-5.077-3.316	c-0.133-2.016,1.927-3.805,4.599-3.996C25.914,27.667,28.187,29.152,28.319,31.169z M24.38,22.453	c-1.591,0.451-3.373-1.062-3.981-3.367c-0.604-2.312,0.194-4.543,1.785-4.992c1.593-0.453,3.374,1.059,3.982,3.367	C26.77,19.77,25.973,22.004,24.38,22.453z"/></svg>',
    "claim_done": '<svg width="14px" height="14px" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path d="M861.588238 240.133873v-65.792823c0-36.191275-29.439775-65.631049-65.631049-65.63105h-21.877358c-36.191275 0-65.631049 29.439775-65.631049 65.63105v65.631049H314.659414v-65.631049c0-36.191275-29.439775-65.631049-65.631049-65.63105h-21.877358c-36.191275 0-65.631049 29.439775-65.631049 65.63105v65.792823c-36.317212 0.868255-65.631049 30.539428-65.63105 67.061417v543.745565c0 37.06772 30.155471 67.223191 67.223191 67.223191h696.886045c37.06772 0 67.223191-30.155471 67.223191-67.223191V307.19529c-0.001024-36.52199-29.315885-66.193162-65.633097-67.061417z m-109.385765-65.792823c0-12.060345 9.817012-21.877358 21.877358-21.877358h21.877358c12.060345 0 21.877358 9.817012 21.877358 21.877358v175.016814c0 12.060345-9.817012 21.877358-21.877358 21.877358h-21.877358c-12.060345 0-21.877358-9.817012-21.877358-21.877358V174.34105z m-546.928824 0c0-12.060345 9.817012-21.877358 21.877358-21.877358h21.877358c12.060345 0 21.877358 9.817012 21.877358 21.877358v175.016814c0 12.060345-9.817012 21.877358-21.877358 21.877358h-21.877358c-12.060345 0-21.877358-9.817012-21.877358-21.877358V174.34105z m678.191947 676.600829c0 12.935767-10.532708 23.468476-23.468476 23.468475H163.111076c-12.935767 0-23.468476-10.532708-23.468476-23.468475V307.19529c0-12.402323 9.677764-22.593054 21.877358-23.415233v65.577807c0 36.191275 29.439775 65.631049 65.631049 65.631049h21.877358c36.191275 0 65.631049-29.439775 65.631049-65.631049v-65.631049h393.789368v65.631049c0 36.191275 29.439775 65.631049 65.631049 65.631049h21.877358c36.191275 0 65.631049-29.439775 65.631049-65.631049v-65.577807c12.19857 0.82218 21.877358 11.012911 21.877358 23.415233v543.746589z" fill="#22C67F" /><path d="M706.719439 478.272194l-48.01715-44.741741-182.28128 195.621482-111.468348-122.615387-48.563905 44.148911 159.469116 172.685427z" fill="#74E8AE" /></svg>',
    "playwright_with_chunk": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#4caf50" d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"/><path fill="#ffc107" d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"/><path fill="#4caf50" d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"/><path fill="#ffc107" d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"/><path fill="#f44336" d="M41.84,15H24v13l-3-1L7.16,13.26H7.14C10.68,7.69,16.91,4,24,4C31.8,4,38.55,8.48,41.84,15z"/><path fill="#dd2c00" d="M7.158,13.264l8.843,14.862L21,27L7.158,13.264z"/><path fill="#558b2f" d="M23.157,44l8.934-16.059L28,25L23.157,44z"/><path fill="#f9a825" d="M41.865,15H24l-1.579,4.58L41.865,15z"/><path fill="#fff" d="M33,24c0,4.969-4.031,9-9,9s-9-4.031-9-9s4.031-9,9-9S33,19.031,33,24z"/><path fill="#2196f3" d="M31,24c0,3.867-3.133,7-7,7s-7-3.133-7-7s3.133-7,7-7S31,20.133,31,24z"/></svg>',
    "excel": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="14" height="14" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#169154" d="M29,6H15.744C14.781,6,14,6.781,14,7.744v7.259h15V6z"/><path fill="#18482a" d="M14,33.054v7.202C14,41.219,14.781,42,15.743,42H29v-8.946H14z"/><path fill="#0c8045" d="M14 15.003H29V24.005000000000003H14z"/><path fill="#17472a" d="M14 24.005H29V33.055H14z"/><g><path fill="#29c27f" d="M42.256,6H29v9.003h15V7.744C44,6.781,43.219,6,42.256,6z"/><path fill="#27663f" d="M29,33.054V42h13.257C43.219,42,44,41.219,44,40.257v-7.202H29z"/><path fill="#19ac65" d="M29 15.003H44V24.005000000000003H29z"/><path fill="#129652" d="M29 24.005H44V33.055H29z"/></g><path fill="#0c7238" d="M22.319,34H5.681C4.753,34,4,33.247,4,32.319V15.681C4,14.753,4.753,14,5.681,14h16.638 C23.247,14,24,14.753,24,15.681v16.638C24,33.247,23.247,34,22.319,34z"/><path fill="#fff" d="M9.807 19L12.193 19 14.129 22.754 16.175 19 18.404 19 15.333 24 18.474 29 16.123 29 14.013 25.07 11.912 29 9.526 29 12.719 23.982z"/></svg>',
    "terminal": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#0277bd" d="M19.847,41.956c-5.629-0.002-11.259,0.024-16.888-0.013c-2.855-0.019-3.374-0.7-2.731-3.525 c2.178-9.58,4.427-19.143,6.557-28.734C7.356,7.112,8.588,5.975,11.312,6C22.57,6.106,33.829,6.034,45.088,6.046 c2.824,0.003,3.298,0.614,2.664,3.511c-2.058,9.406-4.129,18.809-6.236,28.203c-0.789,3.516-1.697,4.187-5.353,4.195 C30.724,41.966,25.285,41.958,19.847,41.956z"/><path fill="#fafafa" d="M25.057 23.922c-.608-.687-1.114-1.267-1.531-1.732-2.43-2.728-4.656-5.27-7.063-7.869-1.102-1.189-1.453-2.344-.13-3.518 1.307-1.16 2.592-1.058 3.791.277 3.34 3.717 6.676 7.438 10.071 11.104 1.268 1.369.972 2.3-.424 3.315-5.359 3.895-10.687 7.833-16.01 11.778-1.196.887-2.337 1.109-3.304-.201-1.066-1.445-.08-2.305 1.026-3.114 3.955-2.893 7.903-5.798 11.834-8.725C23.865 24.83 24.595 24.267 25.057 23.922zM21.75 37C20.625 37 20 36 20 35s.625-2 1.75-2c4.224 0 6.112 0 9.5 0 1.125 0 1.75 1 1.75 2s-.625 2-1.75 2C29.125 37 25 37 21.75 37z"/></svg>'
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
                                                server_function_name = msg_tool_call['function']['name']
                                                if server_function_name.startswith("local"):
                                                    server_name = ''.join(server_function_name.split("-")[1:])
                                                    function_name = ""
                                                elif server_function_name.startswith("pdf-tools"):
                                                    server_name = "pdf-tools"
                                                    function_name = "".join(server_function_name.split("-")[2:])
                                                else:
                                                    server_name, function_name = server_function_name.split("-")
                                                dst.write(icon_map[server_name] if server_name in icon_map else "🛠")
                                                dst.write(f"`{server_name} {function_name}`\n\n")
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