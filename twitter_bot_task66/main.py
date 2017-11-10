import tweepy
import requests
import time
from time import strftime
import json
import datetime
import re

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def main():
    # Fill in the values noted in previous step here
    cfg = {
        "consumer_key": "wDllcVa62ZDTEgNNmyXTiNJTO",
        "consumer_secret": "LMUDV8oHBvBAcl5rsgr5TrnyIEkwEa4gR5P9FOvlf1jmPEQV9C",
        "access_token": "704686666913603584-Dizzy41kubxCwybKopZubhqca0lzsMa",
        "access_token_secret": "YrWAv6dSNbI1cy5WJF2OtHU0xMqyzuFXgRR3HQHV1pKNq"
    }

    date1 = datetime.date(2017, 1, 1)
    date2 = datetime.date(2017, 10, 10)
    day = datetime.timedelta(days=1)

    while date1 <= date2:
        result_json = json.loads(requests.get('http://budget.gov.ru/epbs/registry/grants/data?filterminsum=1000000000&filterminstartdate=' + date1.strftime('%d.%m.%Y')).text)['data']

        date1 = date1 + day
        for subs in result_json:

            target =  subs['info']['regNum']
            sum = subs['plans'][0]['sumTotal']

            tweet = 'Номер транзакции: {0}. Сумма:{1} Узнай больше на http://budget.gov.ru/'.format(target, sum)
            print(tweet)
            api = get_api(cfg)
            status = api.update_status(status=tweet)

        time.sleep(3600*4)
    # Yes, tweet is called 'status' rather confusing


if __name__ == "__main__":
    try:
        while True:

            cfg = {
                "consumer_key": "wDllcVa62ZDTEgNNmyXTiNJTO",
                "consumer_secret": "LMUDV8oHBvBAcl5rsgr5TrnyIEkwEa4gR5P9FOvlf1jmPEQV9C",
                "access_token": "704686666913603584-Dizzy41kubxCwybKopZubhqca0lzsMa",
                "access_token_secret": "YrWAv6dSNbI1cy5WJF2OtHU0xMqyzuFXgRR3HQHV1pKNq"
            }

            print('Введите дату в формате: DD:MM:YYYY')
            inpt = input()
            pattern = re.compile('[0-9]{2}.[0-9]{2}.[0-9]{2}')
            if not pattern.match(inpt):
                print('Дата введена неверно! попробуйте снова')
            else:
                result_json = json.loads(requests.get(
                    'http://budget.gov.ru/epbs/registry/grants/data?filterminsum=1000000000&filterminstartdate={0}&filtermaxstartdate={0}'.format(inpt)).text)

                print(result_json)

                subs = result_json['data'][0]
                target = subs['info']['regNum']
                sum = subs['plans'][0]['sumTotal']

                tweet = ' Test_console Номер транзакции: {0}. Сумма:{1} Узнай больше на http://budget.gov.ru/'.format(target, sum)
                print(tweet)
                api = get_api(cfg)
                try:
                    status = api.update_status(status=tweet)
                except Exception as e:
                    print('Сообщение об этом уже содержится в Твиттер-аккаунте')

    except:
        pass
    main()
