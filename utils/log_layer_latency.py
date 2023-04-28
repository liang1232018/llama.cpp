import re
import argparse

import matplotlib.pyplot as plt

import numpy as np

parser = argparse.ArgumentParser(description='An example program.')
parser.add_argument('--input', type=str, required=True, help='Input file path')
args = parser.parse_args()

layer_map = {}

with open(args.input, 'r') as f:
    for line in f:
        numbers = re.findall(r'\d+\.\d+|\d+', line)
        # 输出结果：['22', '21', '0.002000']
        
        if numbers[1] != '20':
            continue

        if numbers[0] in  layer_map:
            layer_map[numbers[0]].append(float(numbers[2]))
        else:
            layer_map[numbers[0]] = [ float(numbers[2])]


layer_average_map = {}

for k,v in layer_map.items():

    layer_average_map[k] = np.mean(np.array(v))

    plt.clf()

    fig, ax = plt.subplots(1,1, figsize=(10, 8))
    x = range(0, len(v))
    ax.plot(x, v, label=k)

    plt.legend()
    plt.savefig('logs/layer-latency/llama-6b-matmul-latency-layer-'+k+'.pdf', bbox_inches='tight', pad_inches=0)

sorted_dict = sorted(layer_average_map.items(), key=lambda x: x[1], reverse=True)

# 输出前三个键值对的键
for i in range(15):
    print(sorted_dict[i][0])
    print(str(sorted_dict[i][1])+'ms')