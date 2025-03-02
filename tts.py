import os
import re
import requests
import time
from gtts import gTTS
import urllib3
import socks
import socket
import random
import glob

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_proxy():
    """
    自动配置代理网络
    尝试多种常见代理配置方式
    """
    try:
        # 尝试使用系统代理
        print("正在尝试使用系统代理...")
        # 方法1: 使用环境变量设置HTTP代理
        os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
        os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
        
        # 方法2: 使用SOCKS代理
        # 创建原始socket的引用
        original_socket = socket.socket
        
        # 尝试配置SOCKS5代理
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7890)
        socket.socket = socks.socksocket
        
        # 测试代理连接
        try:
            test_response = requests.get("https://www.google.com", timeout=5, verify=False)
            if test_response.status_code == 200:
                print("代理配置成功！")
                return True
        except Exception as e:
            print(f"代理测试失败: {e}")
            # 恢复原始socket
            socket.socket = original_socket
            
            # 尝试其他常见代理端口
            common_ports = [1080, 8080, 8118, 10809]
            for port in common_ports:
                try:
                    print(f"尝试端口 {port}...")
                    os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
                    os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
                    test_response = requests.get("https://www.google.com", timeout=5, verify=False)
                    if test_response.status_code == 200:
                        print(f"代理配置成功！使用端口: {port}")
                        return True
                except:
                    continue
        
        print("无法自动配置代理，请手动设置代理后重试")
        return False
    except Exception as e:
        print(f"代理配置过程中出现错误: {e}")
        return False

def extract_dharanis(file_path):
    """
    从文件中提取陀罗尼标题和罗马拼音
    返回字典 {标题: 罗马拼音}
    """
    dharanis = {}
    current_title = None
    current_roman = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:  # 跳过空行
                continue
                
            # 检查是否为标题行：以M开头 或 包含"陀罗尼" 或 包含"真言"
            is_title = line.startswith('M') or '陀罗尼' in line or '真言' in line
            
            if is_title:
                # 如果已有上一个标题，保存其罗马拼音
                if current_title and current_roman:
                    # 合并所有行并清理罗马拼音
                    roman_text = ' '.join(current_roman)
                    # 移除中文字符和数字，但保留原始空格
                    roman_text = re.sub(r'[\u4e00-\u9fff]+', '', roman_text)  # 移除中文
                    roman_text = re.sub(r'\d+', '', roman_text)  # 移除数字
                    # 不再规范化空格，保留原始空格格式
                    roman_text = roman_text.strip()  # 仅移除首尾空格
                    
                    dharanis[current_title] = roman_text
                
                # 设置新的当前标题和空的罗马拼音列表
                current_title = line
                current_roman = []
            else:
                # 如果不是标题行，且当前有标题，则添加到罗马拼音
                if current_title:
                    current_roman.append(line)
        
        # 处理最后一个标题
        if current_title and current_roman:
            roman_text = ' '.join(current_roman)
            roman_text = re.sub(r'[\u4e00-\u9fff]+', '', roman_text)  # 移除中文
            roman_text = re.sub(r'\d+', '', roman_text)  # 移除数字
            # 不再规范化空格，保留原始空格格式
            roman_text = roman_text.strip()  # 仅移除首尾空格
            
            dharanis[current_title] = roman_text
    
    except Exception as e:
        print(f"提取陀罗尼时出错: {e}")
    
    return dharanis

def convert_to_audio(dharanis, output_dir='audio_files'):
    """
    将陀罗尼罗马拼音转换为罗马尼亚语音频
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    success_count = 0
    failed_items = []
    
    for title, roman_text in dharanis.items():
        try:
            # 清理文件名
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
            output_file = os.path.join(output_dir, f"{safe_title}.mp3")
            
            print(f"正在转换: {title}")
            print(f"罗马拼音: {roman_text}")
            
            # 使用gTTS将文本转换为语音（使用罗马尼亚语）
            tts = gTTS(text=roman_text, lang='ro', slow=False)
            tts.save(output_file)
            
            print(f"已保存到: {output_file}")
            success_count += 1
            
            # 添加随机延迟，避免API限制
            time.sleep(random.uniform(1.0, 3.0))
            
        except Exception as e:
            print(f"转换失败 '{title}': {e}")
            failed_items.append((title, str(e)))
    
    return success_count, failed_items

def process_file(file_path):
    """
    处理单个文件
    """
    # 获取文件名（不带扩展名）用作输出目录
    base_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_dir = f"audio_{file_name_without_ext}"
    
    print(f"\n正在处理文件: {file_path}")
    print(f"输出目录: {output_dir}")
    
    # 提取陀罗尼数据
    dharanis = extract_dharanis(file_path)
    print(f"从 {file_path} 中提取到 {len(dharanis)} 个陀罗尼")
    
    if not dharanis:
        print("未找到陀罗尼数据，请检查输入文件")
        return 0, 0, []
    
    # 转换为音频
    success_count, failed_items = convert_to_audio(dharanis, output_dir)
    
    # 输出结果统计
    print(f"\n{file_path} 转换完成!")
    print(f"成功: {success_count}/{len(dharanis)}")
    
    if failed_items:
        print(f"失败: {len(failed_items)}")
        print("失败项目:")
        for title, error in failed_items:
            print(f"  - {title}: {error}")
    
    # 返回三个值：成功数量、总数量和失败项目详情（包含文件信息）
    file_failed_items = [(file_path, title, error) for title, error in failed_items]
    return success_count, len(dharanis), file_failed_items

def main():
    # 设置代理
    if not setup_proxy():
        print("警告: 代理设置失败，将尝试直接连接...")
    
    # 获取当前目录下的所有txt文件
    txt_files = glob.glob("*.txt")
    
    if not txt_files:
        print("当前目录下未找到txt文件")
        return
    
    print(f"发现 {len(txt_files)} 个txt文件:")
    for file in txt_files:
        print(f"  - {file}")
    
    total_success = 0
    total_dharanis = 0
    all_failed_items = []  # 收集所有文件处理失败的项目
    file_status = {}  # 记录每个文件的处理状态
    
    # 处理每个txt文件
    for file_path in txt_files:
        try:
            success, total, failed_items = process_file(file_path)
            total_success += success
            total_dharanis += total
            
            # 收集失败项目
            all_failed_items.extend(failed_items)
            
            # 记录文件处理状态
            file_status[file_path] = {
                "total": total,
                "success": success,
                "failed": total - success,
                "status": "完成" if total > 0 else "无数据"
            }
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            file_status[file_path] = {
                "total": 0,
                "success": 0,
                "failed": 0,
                "status": f"处理错误: {str(e)}"
            }
    
    # 总结果
    print("\n" + "="*50)
    print("全部处理完成!")
    print("="*50)
    
    # 文件处理概况
    print("\n文件处理概况:")
    print("-"*50)
    for file_path, status in file_status.items():
        print(f"文件: {file_path}")
        print(f"  状态: {status['status']}")
        if status['total'] > 0:
            print(f"  成功转换: {status['success']}/{status['total']} ({status['success']/status['total']*100:.2f}%)")
    print("-"*50)
    
    # 总计结果
    if total_dharanis > 0:
        success_rate = total_success/total_dharanis*100
        print(f"\n总计成功转换: {total_success}/{total_dharanis} 个陀罗尼 ({success_rate:.2f}%)")
    else:
        print("\n没有找到可转换的陀罗尼")
    
    # 输出所有失败条目的详细信息
    if all_failed_items:
        print("\n所有转换失败的陀罗尼:")
        print("="*50)
        for file_path, title, error in all_failed_items:
            print(f"文件: {file_path}")
            print(f"标题: {title}")
            print(f"错误: {error}")
            print("-"*50)
        
        # 创建失败记录文件
        try:
            with open("failed_conversions.txt", "w", encoding="utf-8") as f:
                f.write(f"转换失败的陀罗尼总计: {len(all_failed_items)}\n")
                f.write("="*50 + "\n")
                for file_path, title, error in all_failed_items:
                    f.write(f"文件: {file_path}\n")
                    f.write(f"标题: {title}\n")
                    f.write(f"错误: {error}\n")
                    f.write("-"*50 + "\n")
            print(f"\n已将失败记录保存到: failed_conversions.txt")
        except Exception as e:
            print(f"保存失败记录时出错: {e}")

if __name__ == "__main__":
    main()