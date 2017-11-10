import matplotlib.pyplot as plt
import json

data = {}
with open('result.json') as data_file:



    data = json.load(data_file)


print(data)

plt.bar(range(len(data)), data.values(), align='center')
plt.xticks(range(len(data)), data.keys())

plt.show()
