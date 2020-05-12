import csv
import re
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from transliterate import translit


def database_generate(db_name='database.csv'):
    database = defaultdict(dict)
    with open(db_name) as f:
        database_raw = csv.DictReader(f)
        for row in database_raw:
            database[row['PRODUCER']][row['MODEL']] = row
            database[translit(row['PRODUCER'], 'ru')] = database[row['PRODUCER']]
    return database


def parse_ce_file(ce_path):
    res = set()
    with open(ce_path, encoding='utf-8') as f:
        content = f.readlines()

    for line in content:
        res.add(line.strip())
    return res


def get_custom_entities(ce_path='custom_entities'):
    ce_files = [(join(ce_path, f), f) for f in listdir(ce_path) if isfile(join(ce_path, f))]
    ce = {}
    for sitemap_file in ce_files:
        ce[sitemap_file[1]] = parse_ce_file(sitemap_file[0])
    return ce


def prepare_ans(ans):
    ans = ans.lower().strip()
    regex_filter = re.compile('[^a-zа-яё\s]')
    ans = regex_filter.sub('', ans)
    regex_spaces = re.compile('\s+')
    return  regex_spaces.sub(' ', ans)


def parse_producer(ans, database):
    ans = ans.split()
    for word in ans:
        if word in database:
            return word, database[word]


def parse_ce(ans, ce, ce_type):
    for ce_current in ce[ce_type]:
        if ce_current in ans:
            return True
    return False


def main():
    database = database_generate()
    ce = get_custom_entities()
    ans = prepare_ans(input("Что надо?\n"))
    producer_name, producer_data = parse_producer(ans, database)

    confirmation = False
    while not confirmation:
        ans = prepare_ans(input("Ты точно хочешь {}?\n".format(producer_name)))
        if parse_ce(ans, ce, 'yes'):
            confirmation = True
            print("О, да ты шаришь! Зацени, что у меня есть:")
            for model in producer_data:
                print(model)

        elif parse_ce(ans, ce, 'no'):
            print("Ну как хочешь")
            exit(0)
        else:
            print("Ничё не понял, давай заново")

    ans = prepare_ans(input("Нужна конкретная модель? Если да, то напиши её название точно так же как в списке выше.\n"))
    if ans in producer_data:
        print("Отличный выбор! {MODEL} обладает встроенной памятью объёмом {INTERNAL_MEMORY}, ёмкостью батареи {BATTERY_CAPASITY}, "
              "а камера обладает целыми {MAIN_CAMERA} мегапикселями! Только сегодня и только для тебе я готов продать этот прекрассный смартфон на операционной "
              "системе {OS} всего за {COST}!".format(**producer_data[ans]))




if __name__ == '__main__':
    main()