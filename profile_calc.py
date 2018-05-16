import diff_calc
import requests
import pp_calc
import sys
import b_info
import configparser
import profile_map_calc
from beatmap import Beatmap


def return_values(user):
    try:
        f = open('keys.cfg');
        config = configparser.ConfigParser()
        config.readfp(f)
        key = config._sections["osu"]['api_key']
    except:
        raise Exception("Invalid config")

    url = 'https://osu.ppy.sh/api/get_user_best?k={}&u={}&limit=5'.format(key, user)
    jsonurl = str(requests.get(url).text)
    jsonurl = jsonurl[1:-2]
    maps_split = [i[1:] for i in jsonurl.split("},")]
    maps_info = []
    for i in range(len(maps_split)):
        maps_info.append([])
        info_list = maps_split[i].split(",")
        maps_info[i] = [(x.split(":")[0][1:-1], x.split(":")[1][1:-1]) for x in info_list]

    pp_info = []

    number = 0

    for i in maps_info:
        beatmap_id = int(i[0][1])
        combo = int(i[2][1])
        c100 = int(i[4][1])
        c50 = int(i[3][1])
        miss = int(i[6][1])
        mods = int(i[10][1])

        number += 1
        print number


        pp_info.append(profile_map_calc.return_values(c100, c50, miss, combo, beatmap_id, mods))

    return pp_info