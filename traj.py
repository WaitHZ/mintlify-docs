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
        target_md = f_prefix + "__.mdx"
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
                        
                        model_name = log_path.split("/")[-1].replace(".json", "")
                        dst.write(f"<Accordion title=\"{model_name}\">\n\n")

                        dst.write(f"<Columns cols={2}>\n")
                        if log_data["pass"]:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"check\">\n")
                            dst.write(f"Completed\n")
                        else:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"cross\">\n")
                            dst.write(f"Failed\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Tool Calls\" icon=\"wrench\">\n")
                        dst.write(f"3\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"</Columns>\n")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_dir", type=str, default="docs/tasks")
    args = parser.parse_args()
    main(args)