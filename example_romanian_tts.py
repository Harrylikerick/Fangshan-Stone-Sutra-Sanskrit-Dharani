#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
罗马尼亚语文本转语音示例脚本
这个脚本展示了如何使用romanian_tts.py进行文本到罗马尼亚语音频的转换
"""

import os
import subprocess
import time

def main():
    print("="*50)
    print("罗马尼亚语文本转语音示例")
    print("="*50)
    
    # 示例1：从文件转换
    print("\n示例1：从文件转换")
    print("-"*50)
    
    # 创建示例文本文件
    example_text = """
Bună ziua! Acesta este un exemplu de text în limba română.
Sper că vă place acest instrument de conversie text-în-vorbire.
Puteți converti orice text în limba română în fișiere audio.
    """
    
    # 保存示例文本到文件
    example_file = "example_romanian.txt"
    with open(example_file, "w", encoding="utf-8") as f:
        f.write(example_text)
    
    print(f"已创建示例文件: {example_file}")
    print(f"文件内容:\n{example_text}")
    
    # 调用romanian_tts.py处理文件
    print("\n正在将文件转换为罗马尼亚语音频...")
    subprocess.run(["python", "romanian_tts.py", "-f", example_file])
    
    # 示例2：直接转换文本
    print("\n\n示例2：直接转换文本")
    print("-"*50)
    
    direct_text = "Aceasta este o demonstrație directă a conversiei text-în-vorbire în limba română."
    print(f"示例文本: {direct_text}")
    
    # 调用romanian_tts.py处理直接输入的文本
    print("\n正在将文本转换为罗马尼亚语音频...")
    output_file = f"direct_example_{int(time.time())}.mp3"
    subprocess.run(["python", "romanian_tts.py", "-t", direct_text, "-o", output_file])
    
    # 示例3：使用慢速选项
    print("\n\n示例3：使用慢速选项")
    print("-"*50)
    
    slow_text = "Acesta este un exemplu de vorbire lentă în limba română."
    print(f"示例文本: {slow_text}")
    
    # 调用romanian_tts.py处理文本，使用慢速选项
    print("\n正在将文本转换为慢速罗马尼亚语音频...")
    slow_output_file = f"slow_example_{int(time.time())}.mp3"
    subprocess.run(["python", "romanian_tts.py", "-t", slow_text, "-o", slow_output_file, "-s"])
    
    print("\n\n所有示例已完成！")
    print("="*50)
    print("生成的音频文件:")
    print(f"1. romanian_audio_example_romanian/example_romanian.mp3")
    print(f"2. {output_file}")
    print(f"3. {slow_output_file}")
    print("="*50)

if __name__ == "__main__":
    main() 