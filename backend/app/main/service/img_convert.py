import base64

def base64_convert(path):
    encoded = base64.b64encode(open(path, "rb").read())
    # print(encoded)
    # print(type(encoded))
    return str(encoded)

num = 15

data = base64_convert("sample_img/house/sample_house"+str(num)+".png")
data = data[2:-1]

f = open("sample_img/house/sample_house"+str(num)+".txt", 'w')
f.write(data)
f.close()