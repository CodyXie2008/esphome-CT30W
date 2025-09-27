import sys
import re

# 从文件读取pronto数据
with open('temp_pronto_data.txt', 'r') as f:
    input_string = f.read()

print("input esphome web portal output of pronto data:")
print("---------------------------")
print(input_string)

print("")
print("result")
print("-"*30)
match_pronto_char = re.findall(r"[A-F0-9]{4}", input_string)
print(" ".join(match_pronto_char))