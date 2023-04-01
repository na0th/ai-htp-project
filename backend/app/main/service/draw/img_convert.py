import base64

def base64_convert(path):
    encoded = base64.b64encode(open(path, "rb").read())
    # print(encoded)
    # print(type(encoded))
    return str(encoded)

data = base64_convert("sample_img/tree/sample_tree2.png")
data = data[2:-1]

f = open("sample_img/tree/sample_tree2.txt", 'w')
f.write(data)
f.close()