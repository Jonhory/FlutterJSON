# -*- coding: utf-8 -*-

import json
import sys
import os

# 全部变量 [{key: className, value: dict}]保存已处理的字典类型 ，用于过滤相同数据的重复处理
writeDictList = []


def readFile(path, name = 'Bean0'):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        f.close()
        js = json.dumps(content)
        resource = json.loads(js)

        data = json.loads(resource)

        # 通用头部
        result = """import 'package:json_annotation/json_annotation.dart';\n"""
        result += """part '%s.g.dart';\n""" % name

        if type(data) is dict:
            print('开始解析 字典json')
            result = analysisDict(data, result, name)
        elif type(data) is list:
            print('开始解析 数组json')
            if (len(data)) > 0:
                result = analysisDict(data[0], result, name)
            else:
                print('数组为空')

        print(result)
        saveFile(result, path, 'dart')


def analysisDict(dic, result, className):
    if checkRepeatDic(dic)[0]:
        return result

    writeDictList.append({'key': className, 'value': dic})

    result += """\n@JsonSerializable()\n"""
    result += 'class ' + className + ' {\n'

    resultList = analysisOneDict(dic, result, className)
    result = resultList[0]
    otherlist = resultList[1]
    result += '\n}\n'

    for item in otherlist:
        if type(item) is dict:
            for key, value in item.items():
                if type(value) is dict:
                    result = analysisDict(value, result, key.capitalize() + 'Bean')
                elif type(value) is list:
                    if len(value) > 0:
                        if type(value[0]) is dict:
                            print('开始解析 ' + key)
                            result = analysisDict(value[0], result, key.capitalize() + 'Bean')
                        else:
                            print('警告，此数据结构异常')

    return result


# 解析一个字典数据
def analysisOneDict(dic, result, className):
    # 装 value = dict 或 list 的数据
    otherlist = []

    classinit = '  ' + className + '(\n'

    # 遍历字典
    for k, v in dic.items():
        if type(v) == str:
            result += '  '
            result += 'String ' + k + ';\n'
        elif type(v) == int:
            result += '  '
            result += 'int ' + k + ';\n'
        elif type(v) == float:
            result += '  '
            result += 'double ' + k + ';\n'
        elif type(v) == bool:
            result += '  '
            result += 'bool ' + k + ';\n'
        elif v is None:
            result += '  '
            result += 'String ' + k + ';\n'
        elif type(v) is dict:
            result += '  '
            check = checkRepeatDic(v)
            if check[0]:
                result += check[1] + ' ' + k + ';\n'
            else:
                result += k.capitalize() + 'Bean ' + k + ';\n'
            otherlist.append({k: v})
        elif type(v) is list:
            result += '  '
            if len(v) > 0 and type(v[0]) is dict:
                check = checkRepeatDic(v[0])
                if check[0]:
                    result += 'List<' + check[1] + '> ' + k + ';\n'
                else:
                    result += 'List<' + k.capitalize() + 'Bean> ' + k + ';\n'
                otherlist.append({k: v})
            else:
                result += 'List ' + k + ';\n'

        else:
            print(k, '========', v)
            print(type(v))

        classinit += '    this.' + k + ',\n'

    classinit += '  );\n'
    result += '\n' + classinit

    result += '  factory  ' + className + ' .fromJson(Map<String, dynamic> json) =>\n'
    result += '    _$ ' + className + ' FromJson(json);\n'
    result += '\n'
    result += '  Map<String, dynamic> toJson() => _$ ' + className + ' ToJson(this);'

    return [result, otherlist]


# 查重
def checkRepeatDic(dic):
    for dicc in writeDictList:
        # 差集
        differ = set(dicc['value'].keys()) - set(dic.keys())
        if len(differ) == 0:
            print('重复的类：%s' % dicc['key'])
            return [True, dicc['key']]
    return [False, '']


# 保存文件
def saveFile(content, path, suffix):
    p = os.path.split(path)
    file = p[1].split('.')[0]
    newFile = p[0] + "/" + file + suffix
    with open(newFile, "w", encoding="utf-8") as f:
        f.write(content)
        print('生成成功: path = ', newFile)


if __name__ == "__main__":
    print('使用方法 python3 ${py脚本路径} ${json文件路径} ${初始类名}')

    test = True
    if test:
        readFile('/Users/user/Desktop/json.md', 'TestBean')
    else:
        if len(sys.argv) == 1:
            print('请输入json文件路径')
        elif len(sys.argv) == 2:
            readFile(sys.argv[1])
        elif len(sys.argv) == 3:
            readFile(sys.argv[1], sys.argv[2])
        else:
            print('请检查输入的参数')
