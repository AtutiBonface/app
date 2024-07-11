
import os
filename = 'c'
cont_type = 'image/jpg'
if cont_type:
    mim_type = cont_type.split(';')[0]
    my_ex = mim_type.split('/')[-1]
    check_file = os.path.basename(filename)
    _name , _ext = os.path.splitext(check_file)

    if not _ext:
        new_name = f'{filename}.{my_ex}'

        filename = new_name