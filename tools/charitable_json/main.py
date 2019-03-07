#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

texts = []
with open("input.txt", "rb") as f:
    lines = f.readlines()
    category = ""
    for line in lines:
        if len(line) > 1:
            category += line
        else:
            texts.append(category)
            category = ""
    texts.append(category)

all_jsons = {}
category_titles = ["教育助学", "扶贫救灾", "医疗救助", "其他"]
index = 0
for text in texts:
    components = text.split("\n")
    category_news = []
    for component in components:
        json_dict = {}
        items = component.split("\t")
        if len(items) != 4:
            print(component)
            continue
        json_dict["title"] = items[0]
        json_dict["desc"] = items[1]
        json_dict["date"] = items[2]
        json_dict["imageUrl"] = items[3]
        # if index > 0:
        #     json_dict["author"] = '戴斌'
        # else:
        #     json_dict["author"] = '网络'
        category_news.append(json_dict)
    category = category_titles[index]
    all_jsons[category] = category_news
    index += 1
json_str = json.dumps(all_jsons, ensure_ascii=False, indent=4)
print(json_str)
with open("charitable.json", "wb") as f:
    f.write(json_str)
