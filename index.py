txt = "/r obdal"

if txt.find('/r') == 0 and txt[2] == " ":
    name = txt.split()[1]
    print("rosting "+name)
