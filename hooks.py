from pathlib import Path

def generate_nav(config, **kwargs):
    """自动遍历docs目录生成导航，支持文件夹层级"""
    docs_dir = Path(config["docs_dir"])
    nav = []
    
    # 按你的一级文件夹顺序定义（与实际文件夹名完全匹配）
    root_folders = [
        "编程语言",
        "计算机基础",
        "网络空间安全",
        "测试"
    ]
    
    for folder in root_folders:
        folder_path = docs_dir / folder
        if not folder_path.exists():
            continue  # 跳过不存在的文件夹
        
        # 遍历文件夹下的所有md文件
        files = []
        for md_file in sorted(folder_path.glob("*.md")):
            # 生成相对路径（如 "Coding Language/C.md"）
            rel_path = str(md_file.relative_to(docs_dir)).replace("\\", "/")  # 适配Windows路径
            # 用文件名作为标题（去掉.md）
            title = md_file.stem
            files.append({title: rel_path})
        
        # 将文件夹和文件添加到导航
        nav.append({folder: files})
    
    # 覆盖配置中的nav
    config["nav"] = nav