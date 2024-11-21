import re
import math

# ファイル名
file_name = "[path]"

# ファイルを開いてテキストを読み込む
with open(file_name, 'r') as file:
    input_text = file.read()

# 正規表現を使用して最後のファイルサイズを抽出
file_size_pattern = re.compile(r'(\d+\.\d+G)\s+\d+%\s+(\d+\.\d+)MB/s\s+\d+:\d+:\d+')
matches = file_size_pattern.findall(input_text)

if matches:
    last_file_size_gigabytes = float(matches[-1][0][:-1])  # ギガバイト単位のファイルサイズ
    last_file_size_megabytes = float(matches[-1][1])      # メガバイト単位のファイルサイズ
    file_size_in_megabytes = last_file_size_gigabytes * 1024 + last_file_size_megabytes
    file_size_in_kilobytes = int(round(file_size_in_megabytes * 1024))  # 整数に四捨五入してKB単位に変換
    print(file_size_in_kilobytes)  # KB単位で整数値として出力
else:
    print("ファイルサイズが見つかりませんでした。")
