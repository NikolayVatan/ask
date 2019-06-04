import requests
import pymongo
from pymongo import MongoClient
import pprint
from lxml import html


def search(username):
    url = 'https://ask.fm/' + username
    r = requests.get(url)
    client = MongoClient()
    db = client.test_database
    ask = db.ask
    print(ask)
    user = ask.find_one({'username': username})
    if user:
        user.pop('_id', None)
        return user

    # print(i.attribute['class'])

    if 'The specified profile could not be found.' in r.text:
        result = {
            'exists': False
        }
    else:
        result = {
            'exists': True,
            'link': url
        }
        tree = html.fromstring(r.text)
        img = tree.xpath("//div[@class = 'profileBox_header']/a")
        print(img[0].xpath('./@style')[0])
        info = tree.xpath("//section[@class = 'top-content']/ul/li/div")
        kart = ''
        for i in info:
            if i.text is None:
                continue
            txt = i.text
            kart += txt.strip() + ' '
            print(kart)
            print(i.text)

        total = {'photo': img[0].xpath('./@style')[0], 'information': kart, 'username': username, 'url': url}

        ask.insert_one(total)
        total.pop('_id', None)
        return total


if __name__ == '__main__':
    print(search('p_korchagin'))
