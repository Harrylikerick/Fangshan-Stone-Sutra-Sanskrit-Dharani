# 罗马尼亚语文本转语音工具

这是一个简单的工具，可以将文本转换为罗马尼亚语音频，并自动配置代理。

## 功能特点

- 自动尝试配置代理，支持多种常见代理端口
- 支持从文件读取文本或直接输入文本
- 支持自定义输出路径
- 支持调整语速
- 简单易用的命令行界面

## 安装依赖

在使用此工具前，请确保已安装以下Python包：

```bash
pip install gtts requests urllib3 pysocks
```

## 使用方法

### 基本用法

1. 从文件转换文本：

```bash
python romanian_tts.py -f input.txt
```

2. 直接输入文本转换：

```bash
python romanian_tts.py -t "Acesta este un text în limba română"
```

### 高级选项

- 指定输出路径：

```bash
# 指定输出文件
python romanian_tts.py -f input.txt -o output.mp3

# 指定输出目录
python romanian_tts.py -f input.txt -o output_directory
```

- 使用较慢的语速（更清晰）：

```bash
python romanian_tts.py -f input.txt -s
```

- 组合使用：

```bash
python romanian_tts.py -t "Acesta este un text în limba română" -o my_audio.mp3 -s
```

## 命令行参数

- `-f, --file`: 输入文件路径
- `-t, --text`: 直接输入文本
- `-o, --output`: 输出文件或目录路径
- `-s, --slow`: 使用较慢的语速
- `-h, --help`: 显示帮助信息

## 代理配置

该工具会自动尝试配置代理，支持以下常见代理端口：
- 7890
- 1080
- 8080
- 8118
- 10809

工具会自动尝试HTTP和SOCKS5代理，如果配置成功，将使用该代理进行网络连接。如果所有代理配置都失败，工具将尝试直接连接。

## 示例

1. 将文件 `poem.txt` 转换为罗马尼亚语音频，并保存到默认目录：

```bash
python romanian_tts.py -f poem.txt
```

2. 将直接输入的文本转换为罗马尼亚语音频，使用较慢的语速，并保存到指定文件：

```bash
python romanian_tts.py -t "Bună ziua! Cum te simți astăzi?" -s -o greeting.mp3
```

## 注意事项

- 该工具使用Google Text-to-Speech (gTTS) API，需要网络连接
- 如果文本过长，可能需要较长时间处理
- 如果遇到网络问题，请检查代理设置或直接连接网络 