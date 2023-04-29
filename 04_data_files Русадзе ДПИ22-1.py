import json
import os
import pickle
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

path1 = "C:\\Мари\\учеба\\Финансовый университет\\1 курс\\2 семестр\Технологии обработки данных\\Лабораторная работа 3\data\\"
path2 = "C:\\Мари\\учеба\\Финансовый университет\\1 курс\\2 семестр\\Технологии обработки данных\\Лабораторная работа 2\\data\\"

# 1.1 Считайте файл `contributors_sample.json`. Воспользовавшись модулем `json`, преобразуйте содержимое файла в соответствующие объекты python. Выведите на экран информацию о первых 3 пользователях
with open(path1 + "contributors_sample.json", 'r', encoding='utf8') as fp:
    dt1 = json.load(fp)
for i in range(3):
    print(dt1[i]["username"])

# 1.2 Выведите уникальные почтовые домены, содержащиеся в почтовых адресах людей
unique_domens = set()
for human in dt1:
    unique_domens.add(human["mail"].split('@')[-1])
print(unique_domens)

# 1.3 Напишите функцию, которая по `username` ищет человека и выводит информацию о нем. Если пользователь с заданным `username` отсутствует, возбудите исключение `ValueError`
def find_user(data, username):
    try:
        for human in data:
            if human["username"] == username:
                return human
        raise ValueError
    except ValueError:
        return "Пользователя не существует"
print(find_user(dt1, "uhebert"))

# 1.4 Посчитайте, сколько мужчин и женщин присутсвует в этом наборе данных.
M, F = 0, 0
for human in dt1:
    if human['sex'] == 'M':
        M += 1
    else:
        F += 1
print("Количество мужчин:", M)
print("Количество женщин:", F)

# 1.5 Создайте `pd.DataFrame` `contributors`, имеющий столбцы `id`, `username` и `sex`
contributors = pd.DataFrame(columns=['id', "username", 'sex'])
for human in dt1:
    contributors = contributors._append({'id': human["id"], 'username': human["username"], 'sex': human["sex"]},
                                        ignore_index=True)
print(contributors.head())

# 1.6 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Объедините `recipes` с таблицей `contributors` с сохранением строк в том случае, если информация о человеке отсутствует в JSON-файле. Для скольких человек информация отсутствует?
recipes = pd.read_csv(path2 + "recipes_sample.csv", sep=',')
start_len = len(recipes)
recipes = recipes.merge(contributors, left_on="contributor_id", right_on="id", how="left")
recipes = recipes[pd.isnull(recipes['id_y'])]
print(len(recipes["contributor_id"].unique()))

# 2.1 На основе файла `contributors_sample.json` создайте словарь следующего вида: \n",
#     "```\n",
#     "{\n",
#     "    должность: [список username людей, занимавших эту должность]\n",
#     "}\n",
#     "```"
positions = dict()
for human in dt1:
    for job in human['jobs']:
        if job not in positions:
            positions[job] = list()
        positions[job].append(human["username"])

# 2.2 Сохраните результаты в файл `job_people.pickle` и в файл `job_people.json` с использованием форматов pickle и JSON соответственно. Сравните объемы получившихся файлов. При сохранении в JSON укажите аргумент `indent`
with open(path1 + "job_people.pickle", 'wb') as fp:
    pickle.dump(positions, fp)
with open(path1 + "job_people.json", 'w', encoding='utf8') as fp:
    json.dump(positions, fp, indent='\t')
print("job_people.pickle:", os.path.getsize(path1 + "job_people.pickle"))
print("job_people.json:", os.path.getsize(path1 + "job_people.json"))

# 2.3 Считайте файл `job_people.pickle` и продемонстрируйте, что данные считались корректно
with open(path1 + "job_people.pickle", 'rb') as fp:
    buf = pickle.load(fp)
print(buf)

# 3.1 По данным файла `steps_sample.xml` сформируйте словарь с шагами по каждому рецепту вида `{id_рецепта: [\"шаг1\", \"шаг2\"]}`. Сохраните этот словарь в файл `steps_sample.json`
with open(path1 + "steps_sample.xml", 'r') as fp:
    dt2 = BeautifulSoup(fp, 'xml')
dt2_dict = dict()
for recipe in dt2.find_all('recipe'):
    ids = recipe.find('id')
    if ids.text not in dt2_dict:
        dt2_dict[ids.text] = list()
    for step in recipe.find_all('step'):
        dt2_dict[ids.text].append(step.text)
with open(path1 + 'steps_sample.json', 'w', encoding='utf8') as fp:
    json.dump(dt2_dict, fp, indent='\t')

# 3.2 По данным файла `steps_sample.xml` сформируйте словарь следующего вида: `кол-во_шагов_в_рецепте: [список_id_рецептов]`
dt2_dict2 = dict()
for recipe in dt2.find_all('recipe'):
    count_steps = len(recipe.find_all("step"))
    if count_steps not in dt2_dict2:
        dt2_dict2[count_steps] = list()
    dt2_dict2[count_steps].append(recipe.find("id").text)
print(dt2_dict2)

# 3.3 Получите список рецептов, в этапах выполнения которых есть информация о времени (часы или минуты). Для отбора подходящих рецептов обратите внимание на атрибуты соответствующих тэгов
has_time_recipes = list()
for recipe in dt2.find_all('recipe'):
    for step in recipe.find_all("step"):
        if "has_minutes" in step.attrs or "has_hours" in step.attrs:
            has_time_recipes.append(recipe.find('id').text)
            break
print(has_time_recipes)

# 3.4 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Для строк, которые содержат пропуски в столбце `n_steps`, заполните этот столбец на основе файла  `steps_sample.xml`. Строки, в которых столбец `n_steps` заполнен, оставьте без изменений
recipes = pd.read_csv(path2 + "recipes_sample.csv", sep=',')
for rec in dt2.find_all('recipe'):
    idf = rec.find('id').text
    if not recipes[recipes['id'] == int(idf)]['n_steps'].values[0] > 0:
        recipes.loc[recipes['id'] == int(idf), 'n_steps'] = len(rec.find_all('step'))
print(recipes.head())

# 3.5 Проверьте, содержит ли столбец `n_steps` пропуски. Если нет, то преобразуйте его к целочисленному типу и сохраните результаты в файл `recipes_sample_with_filled_nsteps.csv`
if recipes['n_steps'].isnull().sum() == 0:
    recipes['n_steps'] = recipes['n_steps'].astype(np.int64)
    recipes.to_csv(path1 + "recipes_sample_with_filled_nsteps.csv", index=False)

