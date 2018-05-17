import diff_calc
import requests
import pp_calc
import sys
import b_info
import configparser
from beatmap import Beatmap

'''
parser = argparse.ArgumentParser()
feature = False
mod_s = ""
c100 = 0
c50 = 0
misses = 0
sv = 1
acc = 0
combo = 0
parser.add_argument('file', help='File or url. If url provided use -l flag')
parser.add_argument('-l', help='Flag if url provided', action='store_true')
parser.add_argument('-acc', help='Accuracy', metavar="acc%", default=0)
parser.add_argument('-c100', help='Number of 100s', metavar="100s", default=0)
parser.add_argument('-c50', help='Number of 50s', metavar="50s", default=0)
parser.add_argument('-m', help='Number of misses', metavar="miss", default=0, dest='misses')
parser.add_argument('-c', help='Max combo', metavar="combo", default=0, dest='combo')
parser.add_argument('-sv', help='Score version 1 or 2', metavar="sv", default=1)
parser.add_argument('-mods', help='Mod string eg. HDDT', metavar="mods", default="")
args = parser.parse_args()
c100 = int(args.c100)
c50 = int(args.c50)
misses = int(args.misses)
combo = int(args.combo)
acc = float(args.acc)
sv = int(args.sv)
mod_s = args.mods.upper()
feature = args.l
file_name = ""
'''

try:
    f = open('keys.cfg');
    config = configparser.ConfigParser()
    config.readfp(f)
    key = config._sections["osu"]['api_key']
except:
    raise Exception("Invalid config")


def mod_str(mod):
    string = ""
    if mod.nf:
        string += "NF"
    if mod.ez:
        string += "EZ"
    if mod.hd:
        string += "HD"
    if mod.hr:
        string += "HR"
    if mod.dt:
        string += "DT"
    if mod.ht:
        string += "HT"
    if mod.nc:
        string += "NC"
    if mod.fl:
        string += "FL"
    if mod.so:
        string += "SO"
    return string


class mods:
    def __init__(self):
        self.nomod = 0,
        self.nf = 0
        self.ez = 0
        self.hd = 0
        self.hr = 0
        self.dt = 0
        self.ht = 0
        self.nc = 0
        self.fl = 0
        self.so = 0
        self.speed_changing = self.dt | self.ht | self.nc
        self.map_changing = self.hr | self.ez | self.speed_changing

    def update(self):
        self.speed_changing = self.dt | self.ht | self.nc
        self.map_changing = self.hr | self.ez | self.speed_changing


mod = mods()


def set_mods(mod, m):
    if m & 0b1:
        mod.nf = 1
    if m & 0b10:
        mod.ez = 1
    if m & 0b1000:
        mod.hd = 1
    if m & 0b10000:
        mod.hr = 1
    if m & 0b1000000:
        mod.dt = 1
    if m & 0b100000000:
        mod.ht = 1
    if m & 0b1000000000:
        mod.nc = 1
        mod.dt = 0
    if m & 0b10000000000:
        mod.fl = 1
    if m & 0b100000000000:
        mod.so = 1


def return_values(c100, c50, misses, combo, map_id, mod_s):
    global key
    try:
        if key == "":
            print("Please enter an API key to use this feature.")
            raise ()
        file = requests.get("https://osu.ppy.sh/osu/{}".format(map_id)).text.splitlines()
    except:
        print("ERROR: " + file_name + " not a valid beatmap or API key is incorrect")
        sys.exit(1)

    map = Beatmap(file)

    mod.dt = 0
    mod.ez = 0
    mod.fl = 0
    mod.hd = 0
    mod.hr = 0
    mod.ht = 0
    mod.nc = 0
    mod.nf = 0
    mod.so = 0

    if mod_s != 0:
        set_mods(mod, mod_s)
        mod.update()

    mod_string = mod_str(mod)
    map.apply_mods(mod)
    diff = diff_calc.main(map)
    pp, aim_value, speed_value, acc_value, fl_bonus, old_fl_bonus, old_pp, no_fl_pp, no_hd_reb, no_ar_hd = pp_calc.pp_calc(
        diff[0], diff[1],
        diff[3],
        misses,
        c100, c50, mod,
        combo)

    title = map.artist + " - " + map.title + "[" + map.version + "]"
    if mod_string != "":
        title += "+" + mod_string
    title += " (" + map.creator + ")"
    map_s = "Map: {}\n".format(title)
    difficulty_settings = "AR: {:.2f} CS: {:.2f} OD: {:.2f}\n".format(map.ar, map.cs, map.od)
    stars = "Stars: {:.2f}\n".format(diff[2])
    acc = "Acc: {:.2f}%\n\n".format(pp.acc_percent)
    circle_s = "Circles: {}\n".format(map.num_circles)
    slider_s = "Sliders: {}\n".format(map.num_sliders)
    spinner_s = "Spinners: {}\n".format(map.num_spinners)
    object_s = "Objects: {}\n\n".format(map.num_objects)
    comb_s = "Combo: {}/{}\n".format(int(combo), int(map.max_combo))
    miss_s = "Misses: {}\n\n".format(misses)
    aim_vs = "Aim Value: {:.2f}PP\n".format(aim_value)
    speed_vs = "Speed Value: {:.2f}PP\n".format(speed_value)
    acc_vs = "Acc Value: {:.2f}PP\n\n".format(acc_value)
    fl_bs = "Flashlight Aim Bonus: {:.5f}x\n".format(fl_bonus)
    old_fl_bs = "Old Flashlight Aim Bonus: {:.5f}x\n\n".format(old_fl_bonus)
    pp_s = "Performance: {:.2f}PP\n".format(pp.pp)
    old_pp_s = "Old Performance: {:.2f}PP\n".format(old_pp)
    no_fl_pp_s = "No FL Performance: {:.2f}PP\n".format(no_fl_pp)
    no_hd_reb_pp_s = "No HD Rebalance Performance: {:.2f}PP\n".format(no_hd_reb)
    no_ar_hd_pp_s = "No HD AR Rebalance Performance: {:.2f}PP".format(no_ar_hd)

    return (str(title), pp.pp)
