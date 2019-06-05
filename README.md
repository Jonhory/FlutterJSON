# Flutter 中处理json数据

* 配合第三方 `json_annotation` 处理

  To use [package:json_serializable](https://pub.dev/packages/json_serializable) in your package, add these dependencies to your `pubspec.yaml`.

* 使用方法 ` python3 ${py脚本路径} ${json文件路径} ${初始类名} `

* 源文件

```
{
    "name": "BeJson",
    "url": "http://www.bejson.com",
    "page": 88,
    "isNonProfit": true,
    "address": {
        "street": "科技园路.",
        "city": "江苏苏州",
        "country": "中国"
    },
    "links": [
        {
            "name": "Google",
            "url": "http://www.google.com"
        },
        {
            "name": "Baidu",
            "url": "http://www.baidu.com"
        },
        {
            "name": "SoSo",
            "url": "http://www.SoSo.com"
        }
    ]
}
```

* 结果：

```
import 'package:json_annotation/json_annotation.dart';
part 'TestBean.g.dart';

@JsonSerializable()
class TestBean {
  String name;
  String url;
  int page;
  bool isNonProfit;
  AddressBean address;
  List<LinksBean> links;

  TestBean(
    this.name,
    this.url,
    this.page,
    this.isNonProfit,
    this.address,
    this.links,
  );
  factory TestBean .fromJson(Map<String, dynamic> json) =>
    _$ TestBean FromJson(json);

  Map<String, dynamic> toJson() => _$ TestBean ToJson(this);
}

@JsonSerializable()
class AddressBean {
  String street;
  String city;
  String country;

  AddressBean(
    this.street,
    this.city,
    this.country,
  );
  factory AddressBean .fromJson(Map<String, dynamic> json) =>
    _$ AddressBean FromJson(json);

  Map<String, dynamic> toJson() => _$ AddressBean ToJson(this);
}

@JsonSerializable()
class LinksBean {
  String name;
  String url;

  LinksBean(
    this.name,
    this.url,
  );
  factory LinksBean .fromJson(Map<String, dynamic> json) =>
    _$ LinksBean FromJson(json);

  Map<String, dynamic> toJson() => _$ LinksBean ToJson(this);
}
```

* 将`TestBean`、`AddressBean `、`LinksBean ` 更换为开发需要的名称

* 以下方法中故意保留了一个空格符，需要去掉，也可以在源码中自己去掉。

```
  factory TestBean .fromJson(Map<String, dynamic> json) =>
    _$ TestBean FromJson(json);

  Map<String, dynamic> toJson() => _$ TestBean ToJson(this);
```


* 按需要执行相关的操作

```
flutter packages pub run build_runner build
flutter packages pub run build_runner watch
//删除旧文件
flutter packages pub run build_runner build --delete-conflicting-outputs

```


* 当前为测试版本，常见的`json`格式可以正常解析，如果报异常错误，请把`json`和报错信息提交`Issues`
