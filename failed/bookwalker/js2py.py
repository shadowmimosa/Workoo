import jiphy

with open("raw/viewer_loader_2.0.10_2019-09-18.js", "r") as fn:
    js_code = fn.read()

b = jiphy.to.python(js_code)

print(b)
