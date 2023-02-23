from db_connect import db

from models import User, EntireTree, TreeRoot, TreeBranch, TreeLeap, TreeStem, TreeSize

resultJson = {}
resultData = EntireTree.query.filter_by(0).first()
if resultData is not None:
    tmp = resultData.result
    print(type(tmp))
    tmpsplit = resultData.result.split('/')
    print(tmpsplit)
    subtitle = tmpsplit[0]
    print(subtitle)
    print(type(subtitle))
    result = tmpsplit[1]
    print(result)
    print(type(result))
    resultJson.update(dict(subtitle=result))

print(resultJson)