import os
import re
import tts

def main():
    # 只处理1.txt文件
    file_path = "1.txt"
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return
    
    print(f"正在单独处理文件: {file_path}")
    
    # 设置代理
    if not tts.setup_proxy():
        print("警告: 代理设置失败，将尝试直接连接...")
    
    # 使用tts模块处理文件
    success, total, failed_items = tts.process_file(file_path)
    
    # 输出结果统计
    print("\n" + "="*50)
    print(f"文件 {file_path} 处理完成")
    print("="*50)
    print(f"成功转换: {success}/{total} ({success/total*100 if total > 0 else 0:.2f}%)")
    
    # 输出所有失败条目的详细信息
    if failed_items:
        print("\n转换失败的条目:")
        print("="*50)
        for file_path, title, error in failed_items:
            print(f"标题: {title}")
            print(f"错误: {error}")
            print("-"*50)
        
        # 创建失败记录文件
        try:
            with open("failed_single.txt", "w", encoding="utf-8") as f:
                f.write(f"转换失败的陀罗尼总计: {len(failed_items)}\n")
                f.write("="*50 + "\n")
                for file_path, title, error in failed_items:
                    f.write(f"标题: {title}\n")
                    f.write(f"错误: {error}\n")
                    f.write("-"*50 + "\n")
            print(f"\n已将失败记录保存到: failed_single.txt")
        except Exception as e:
            print(f"保存失败记录时出错: {e}")

if __name__ == "__main__":
    main() 