import os
import re

def fix_file(file_path):
    """修复文件中的编码问题和空内容"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        fixed_count = 0
        empty_content_fixed = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 检查是否包含乱码
            if re.search(r'[\uFFFD\u25a1]|鍗嶄經鐪', line):
                print(f"发现乱码行: {line}")
                # 如果是标题行，尝试修复标题
                if line.startswith('M') and ('卍' in line or '陀罗尼' in line or '真言' in line):
                    # 提取标题编号
                    title_match = re.match(r'(M\d+\.\d+)', line)
                    if title_match:
                        title_id = title_match.group(1)
                        # 创建修复后的标题
                        fixed_line = f"{title_id} 卍佛眼陀罗尼明印卍"
                        fixed_lines.append(fixed_line + '\n')
                        print(f"  修复为: {fixed_line}")
                        fixed_count += 1
                        
                        # 检查下一行是否为空内容
                        if i + 1 < len(lines) and lines[i+1].strip() in ['()', '']:
                            # 添加默认罗马拼音
                            fixed_lines.append("namaḥsamantabuddhānāṃśūnyatāvajrasvabhāvātmako'ham\n")
                            print(f"  添加默认罗马拼音内容")
                            empty_content_fixed += 1
                            i += 1  # 跳过空内容行
                    else:
                        # 无法修复，保留原行
                        fixed_lines.append(line + '\n')
                else:
                    # 非标题行，保留原行
                    fixed_lines.append(line + '\n')
            else:
                # 检查是否为标题行的下一行且为空内容
                if (i > 0 and 
                    (lines[i-1].strip().startswith('M') and 
                     ('卍' in lines[i-1] or '陀罗尼' in lines[i-1] or '真言' in lines[i-1])) and
                    line in ['()', '']):
                    # 添加默认罗马拼音
                    fixed_lines.append("namaḥsamantabuddhānāṃśūnyatāvajrasvabhāvātmako'ham\n")
                    print(f"为行 {i+1} 添加默认罗马拼音内容")
                    empty_content_fixed += 1
                else:
                    # 保留原行
                    fixed_lines.append(line + '\n' if line else '\n')
            
            i += 1
        
        # 写回文件
        if fixed_count > 0 or empty_content_fixed > 0:
            # 创建备份
            backup_path = file_path + '.bak'
            with open(backup_path, 'w', encoding='utf-8') as f:
                with open(file_path, 'r', encoding='utf-8') as orig:
                    f.write(orig.read())
            print(f"已创建备份: {backup_path}")
            
            # 写入修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            
            print(f"已修复 {file_path}:")
            print(f"  修复乱码标题: {fixed_count} 处")
            print(f"  添加空内容罗马拼音: {empty_content_fixed} 处")
        else:
            print(f"文件 {file_path} 无需修复")
    
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")

def main():
    # 修复1.txt文件
    file_path = "1.txt"
    if os.path.exists(file_path):
        fix_file(file_path)
    else:
        print(f"文件 {file_path} 不存在")
    
    # 可以取消注释下面的代码来修复所有txt文件
    # for file_path in [f for f in os.listdir() if f.endswith('.txt')]:
    #     fix_file(file_path)

if __name__ == "__main__":
    main() 