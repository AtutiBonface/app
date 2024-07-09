import re,os


f_name = "16668409-uhd_2560_1440_24fps16668409-uhd_2560_1440_24fps.mp4"

name , extension = os.path.splitext(f_name)
if len(name) > 45:
    new_name = f'{name[:20]}...{name[-22:]}{extension}'
    print(new_name)
    print(f_name)



