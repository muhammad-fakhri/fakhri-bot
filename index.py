txt = "/r obdal"
idx = txt.find('/r')

if idx == 0 and txt[2] == " ":
    name = txt.split()[1]
    print("rosting "+name)
    print(idx)
