# function to return key for any value
def get_key(val):
    for url, contenu in l.items():
        print(l.items())
        if val == contenu:
            return url

    return "key doesn't exist"


l = {}
l['url1']="dedbhedbhje"
l['url2']="url2"
l['url3']="url3"
# print(get_key('dedbhedbhje'))
# del l['url1']
del l['url2']
print(l)
