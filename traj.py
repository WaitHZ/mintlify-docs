import argparse
import os
from tqdm import tqdm
import json


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

            dst.write(f"\n<AccordionGroup>\n")

            log_dir = f_prefix + "/"

            for log_file in sorted(os.listdir(log_dir)):
                if log_file.endswith(".json"):
                    log_path = os.path.join(log_dir, log_file)
                    with open(log_path, "r", encoding="utf-8") as lf:
                        log_data = json.load(lf)
                        msgs = log_data["messages"]
                        
                        model_name = log_path.split("/")[-1].replace(".json", "")
                        dst.write(f"<Accordion title=\"{model_name}\">\n\n")

                        dst.write("<Columns cols={2}>\n")
                        if log_data["pass"]:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"check\">\n")
                            dst.write(f"Completed\n")
                        else:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"x\">\n")
                            dst.write(f"Failed\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Tool Calls\" icon=\"wrench\">\n")
                        tool_msgs = [msg for msg in msgs if msg["role"] == "tool"]
                        dst.write(f"{len(tool_msgs)}\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"</Columns>\n\n")

                        for msg in msgs:
                            if msg["role"] == "user":
                                continue
                            elif msg["role"] == "assistant":
                                if msg["content"] == "":
                                    continue
                                dst.write(f"<div className=\"thinking-box\">\n")
                                dst.write(f"🧐{msg['content']}\n</div>\n\n")
                                if "tool_calls" in msg:
                                    msg_tool_call = msg["tool_calls"][0]
                                    if msg_tool_call['type'] == "function":
                                        dst.write(f"<div className=\"tool-call-box\">\n")
                                        dst.write(f"🛠`{msg_tool_call['function']['name']}`\n\n")
                                        dst.write(f"```json\n")
                                        dst.write("{\n")
                                        for i, arg in enumerate(msg_tool_call['function']['arguments'].strip()[1:-1].split(",")):
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
                                    dst.write(f"<div className=\"task-completed-box\">\n")
                                    dst.write(f"📢{msg['content']}\n</div>\n\n")
                            elif msg["role"] == "tool":
                                dst.write(f"<div className=\"result-box\">\n")
                                tool_res = json.loads(msg['content'])
                                if tool_res["type"] != "text":
                                    raise NotImplementedError(f"Unsupported tool call type: {tool_res['type']}")
                                dst.write(f"🔍\n```json\n{tool_res["text"]}\n```\n</div>\n\n")
                            else:
                                raise NotImplementedError(f"Unsupported message role: {msg['role']}")

                        dst.write(f"</Accordion>\n\n")
                    dst.write(f"</AccordionGroup>\n")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_dir", type=str, default="docs/tasks")
    args = parser.parse_args()
    main(args)