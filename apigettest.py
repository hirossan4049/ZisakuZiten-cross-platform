import requests
import json
from pprint import pprint

get_json = requests.get("https://zisakuzitenapi2.herokuapp.com/api/groups/?format=json").json()

print(len(get_json))
ZtitleList = []
GtitleList = []

for i in range(len(get_json)):
    title_list = [get_json[i]["ziten_updT_List"][a]["title"] for a in range(len(get_json[i]["ziten_updT_List"]))]
    ZtitleList.append(title_list)
    GtitleList.append(get_json[i]["title"])

    # for a in range(len(get_json[i]["ziten_updT_List"])):
    #     print(get_json[i]["ziten_updT_List"][a]["title"])

    print("=========")

print(ZtitleList)
print(GtitleList)