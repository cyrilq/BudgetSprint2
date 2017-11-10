import pandas as pd
import requests
import json
import matplotlib.pyplot as plt


post_info = pd.read_csv('data-01-structure-01.csv', delimiter=';', error_bad_lines=False, encoding = 'ISO-8859-1')

inn_list = post_info['INN'].tolist()


result_info = {}

for row in inn_list:
    row = row.strip()

inn_list = filter(None, inn_list)

search_url = 'http://openapi.clearspending.ru/restapi/v3/suppliers/get/?inn='

for row in inn_list:

    try:
        #print(search_url+row)
        result_json = requests.get(search_url+row).text

        result_json = json.loads(result_json)

        try:
            #print(result_json['suppliers']['data'][0]['organizationName'])
            #print(result_json['suppliers']['data'][0]['contractsYearStats']['2017']['contractsSum'])

            result_info[result_json['suppliers']['data'][0]['organizationName']] = \
                result_json['suppliers']['data'][0]['contractsYearStats']['2017']['contractsSum']


        except Exception as e:
            print('ошибка в json')


        #print(result_json)
    except Exception as e:
        print('плохая ссылка')


with open('result.json', 'w') as fp:
    json.dump(result_info, fp)


plt.bar(range(len(result_info)), result_info.values(), align='center')
plt.xticks(range(len(result_info)), result_info.keys())

# plt.show()

with open('result.json') as data_file:
    data = json.load(data_file)
    print(data)
