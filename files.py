import re

file_details = [
    "\n",
    "<file> \n",
    "filename: rihanna.mp4\n",
    "size: 10293944\n",
    "downloaded: 103593\n",
    "status: downloading\n",
    "date-modified: 7/7/2024\n",
    "address: https://imaginekenya.site/rihanna.mp4 \n",
    "path: c:/Users/Bonface/Downloads \n" ,
    "</file>\n",
    "\n",

]
new_details = []
with open('downloading.txt', 'r') as f:
    entry = {}
    for line in f.readlines():
        line.strip()
       
        if line.startswith('<file>'):
            entry = {}

        elif line.startswith('</file>'):
            new_details.append(entry)

            
        else:
            match = re.findall(r'\s*(\S+):\s*(.+)', line)
            if match:
                key , value = match[0]

                entry[key.strip()] = value.strip()

                

            else:
                pass

for detail in range(len(new_details)):
    if new_details[detail]:
        filename,size, status = (new_details[detail]['filename'], new_details[detail]['size'], new_details[detail]['status'])
        print(filename, int(size), status)

            






