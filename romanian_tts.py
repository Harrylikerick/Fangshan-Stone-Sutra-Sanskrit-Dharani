import os
import re
import requests
import time
import random
from gtts import gTTS
import urllib3
import socks
import socket
import argparse

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_proxy():
    """
    自动配置代理网络
    尝试多种常见代理配置方式
    """
    try:
        print("正在尝试自动配置代理...")
        
        # 常见代理端口列表
        proxy_ports = [7890, 1080, 8080, 8118, 10809]
        
        # 尝试HTTP代理
        for port in proxy_ports:
            try:
                print(f"尝试HTTP代理端口 {port}...")
                proxies = {
                    'http': f'http://127.0.0.1:{port}',
                    'https': f'http://127.0.0.1:{port}'
                }
                
                # 设置环境变量
                os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
                os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
                
                # 测试代理连接
                test_response = requests.get("https://www.google.com", 
                                           proxies=proxies, 
                                           timeout=5, 
                                           verify=False)
                
                if test_response.status_code == 200:
                    print(f"HTTP代理配置成功！使用端口: {port}")
                    return True
            except Exception as e:
                print(f"HTTP代理端口 {port} 测试失败: {e}")
        
        # 尝试SOCKS代理
        original_socket = socket.socket  # 保存原始socket引用
        
        for port in proxy_ports:
            try:
                print(f"尝试SOCKS5代理端口 {port}...")
                
                # 配置SOCKS5代理
                socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", port)
                socket.socket = socks.socksocket
                
                # 测试代理连接
                test_response = requests.get("https://www.google.com", timeout=5, verify=False)
                
                if test_response.status_code == 200:
                    print(f"SOCKS5代理配置成功！使用端口: {port}")
                    return True
            except Exception as e:
                print(f"SOCKS5代理端口 {port} 测试失败: {e}")
                # 恢复原始socket
                socket.socket = original_socket
        
        # 恢复原始socket
        socket.socket = original_socket
        print("无法自动配置代理，将尝试直接连接...")
        return False
        
    except Exception as e:
        print(f"代理配置过程中出现错误: {e}")
        return False

def text_to_romanian_audio(text, output_file, slow_speed=False):
    """
    将文本转换为罗马尼亚语音频
    
    参数:
    - text: 要转换的文本
    - output_file: 输出文件路径
    - slow_speed: 是否使用较慢的语速
    
    返回:
    - 成功返回True，失败返回False
    """
    try:
        print(f"正在将文本转换为罗马尼亚语音频...")
        print(f"文本内容: {text[:100]}..." if len(text) > 100 else f"文本内容: {text}")
        
        # 使用gTTS将文本转换为罗马尼亚语音频
        tts = gTTS(text=text, lang='ro', slow=slow_speed)
        tts.save(output_file)
        
        print(f"音频已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def process_file(input_file, output_dir=None, slow_speed=False):
    """
    处理输入文件，将其中的文本转换为罗马尼亚语音频
    
    参数:
    - input_file: 输入文件路径
    - output_dir: 输出目录，如果为None则使用默认目录
    - slow_speed: 是否使用较慢的语速
    """
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 如果未指定输出目录，则使用默认目录
        if output_dir is None:
            # 获取文件名（不带扩展名）用作输出目录
            base_name = os.path.basename(input_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            output_dir = f"romanian_audio_{file_name_without_ext}"
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 构建输出文件路径
        base_name = os.path.basename(input_file)
        file_name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, f"{file_name_without_ext}.mp3")
        
        # 转换为音频
        success = text_to_romanian_audio(text, output_file, slow_speed)
        
        return success
        
    except Exception as e:
        print(f"处理文件 {input_file} 时出错: {e}")
        return False

def process_text(text, output_file=None, slow_speed=False):
    """
    处理输入文本，将其转换为罗马尼亚语音频
    
    参数:
    - text: 输入文本
    - output_file: 输出文件路径，如果为None则使用默认路径
    - slow_speed: 是否使用较慢的语速
    """
    try:
        # 如果未指定输出文件，则使用默认文件
        if output_file is None:
            # 创建输出目录
            output_dir = "romanian_audio_direct"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 使用时间戳作为文件名
            timestamp = int(time.time())
            output_file = os.path.join(output_dir, f"romanian_text_{timestamp}.mp3")
        
        # 转换为音频
        success = text_to_romanian_audio(text, output_file, slow_speed)
        
        return success
        
    except Exception as e:
        print(f"处理文本时出错: {e}")
        return False

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将文本转换为罗马尼亚语音频')
    
    # 添加命令行参数
    parser.add_argument('-f', '--file', help='输入文件路径')
    parser.add_argument('-t', '--text', help='直接输入文本')
    parser.add_argument('-o', '--output', help='输出文件或目录路径')
    parser.add_argument('-s', '--slow', action='store_true', help='使用较慢的语速')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 设置代理
    setup_proxy()
    
    # 处理输入
    if args.file:
        # 处理文件
        if args.output:
            # 检查输出路径是否以.mp3结尾
            if args.output.endswith('.mp3'):
                # 确保输出目录存在
                output_dir = os.path.dirname(args.output)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # 直接使用指定的输出文件
                with open(args.file, 'r', encoding='utf-8') as f:
                    text = f.read()
                success = text_to_romanian_audio(text, args.output, args.slow)
            else:
                # 使用指定的输出目录
                success = process_file(args.file, args.output, args.slow)
        else:
            # 使用默认输出目录
            success = process_file(args.file, None, args.slow)
        
        if success:
            print("文件处理成功！")
        else:
            print("文件处理失败！")
    
    elif args.text:
        # 处理直接输入的文本
        if args.output:
            success = process_text(args.text, args.output, args.slow)
        else:
            success = process_text(args.text, None, args.slow)
        
        if success:
            print("文本处理成功！")
        else:
            print("文本处理失败！")
    
    else:
        # 如果没有提供输入，显示帮助信息
        parser.print_help()

if __name__ == "__main__":
    main() 