import random


def random_rgb_txt():
    rgb_txt = 'rgb('
    a, b, c = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)    
    rgb_txt += str(a)+","
    rgb_txt += str(b)+","
    rgb_txt += str(c)+")"
    return rgb_txt
