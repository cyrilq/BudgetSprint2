import requests
import json


class GetInfoAboutOrganisation:



    def __init__(self, id_org, type_id_org):
        print(id_org)
        self.id = id_org
        self.type_id = type_id_org


    def return_info(self):

        result_answer = ''
        request_string = 'http://openngo.ru/api/organizations/'

        print(self.id, self.type_id)

        if self.type_id == 'inn':

            request_string += '?inn=' + str(self.id)
            print(request_string)

            result_answer = self.create_request(request_string)



        if self.type_id == 'orgn':

            request_string += '?orgn=' + str(self.id)
            print(request_string)

            result_answer = self.create_request(request_string)


        if self.type_id == 'name':

            request_string += '?string_search=' + str(self.id).replace(' ', '+').lower()
            print(request_string)

            result_answer = self.create_request(request_string)



        return result_answer

    def create_pp_doc(self, inn):
        try:
            result_url = 'http://budget.gov.ru/epbs/registry/grants/attachment?id='

            req_url = 'http://budget.gov.ru/epbs/registry/grants/data?blocks=doc&filterinn=' + str(inn)

            result_json = json.loads(requests.get(req_url).text)['data'][0]['documents']

            doc_id = ''

            for doc in result_json:
                if 'ПП_' in doc['name']:
                   doc_id = doc['id']


            if doc_id == '':

               return 'У этой организации нет платежного поручения '

            else:

                return result_url + doc_id

        except Exception as e:
            print('ошибка с платежным поручением')

            return 'У этой организации нет платежного поручения '

    def create_request(self, request_string):



        try:

            result_answer = ''

            result_text = requests.get(request_string).text
            print(result_text)
            result_json = json.loads(result_text)
            print(result_json)



            print(result_json['results'][0]['name'])

            result_pp_doc = self.create_pp_doc(result_json['results'][0]['inn'])
            print(result_pp_doc)


            result_answer = '''
Название организации: {0}
Регион: {1}
Тип: {2}
Статус: {3}
ИНН: {4}
КПП: {5}
ОГРН: {6}
Информация об источниках финансирования и общей сумме финансирования в формате: “Контракты {9} рублей, субсидии {8} рублей, гранты {7} рублей. Общая сумма: {10} рублей”
Ссылка на карточку организации на сайте проекта “Открытые НКО”: {11}
Ссылка на платежное поручение: {12}
            '''.format(result_json['results'][0]['name'],
                       result_json['results'][0]['region']['name'],
                       result_json['results'][0]['type']['name'],
                       'Активна' if result_json['results'][0]['active'] else 'Неактивна',
                       result_json['results'][0]['inn'],
                       result_json['results'][0]['kpp'],
                       result_json['results'][0]['ogrn'],
                       result_json['results'][0]['money_transfers_sum_by_type']['Grant'],
                       result_json['results'][0]['money_transfers_sum_by_type']['Subsidy'],
                       result_json['results'][0]['money_transfers_sum_by_type']['Contract'],
                       result_json['results'][0]['money_transfers_sum'],
                       'http://openngo.ru/organization/{}'.format(result_json['results'][0]['ogrn']),
                       result_pp_doc
                       )

            return result_answer
        except Exception as e:

            print('Скорее всего такой компании нет в нашем реестре')

            return 'Скорее всего такой компании нет в нашем реестре'


