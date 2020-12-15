""" convert a list of python objects to JSON by using a 'jsonify' method on each item """
def jsonifyList(list, name):
    json = ""
    for obj in list:
        json += obj.jsonify() + ","
    json = json[:-1] # remove trailing comma
    json = '{"%s":[%s]}' % (name, json)
    return json
