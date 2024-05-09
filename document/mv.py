import os
import shutil

def move_files(root_dir, new_dir):
  for filename in os.listdir(root_dir):
    file_path = os.path.join(root_dir, filename)
    # 检查文件是否为目录，如果是目录则递归处理
    if os.path.isdir(file_path):
      move_files(file_path, new_dir)
    else:
      # 检查文件是否在根目录下
      if os.path.dirname(file_path) == root_dir:
        # 构建新的文件路径
        new_path = os.path.join(new_dir, filename)
        # 移动文件
        shutil.move(file_path, new_path)


dir1 = "/mnt/data1/zc_data/dianchang/dianchang_06/dianchang_jlw_0619/dianchang"
dir2 = "/mnt/data1/zc_data/dianchang/dianchang_06/dianchang_jlw_0619/all_data"

move_files(dir1, dir2)