# 本地服务连接信息

> 以下连接信息仅用于本地开发环境。

## Redis

| 配置项 | 值 |
| --- | --- |
| 地址 | `127.0.0.1` |
| 端口 | `16379` |
| 密码 | `123456` |
| 数据库 | `0` |

连接 URL：

```text
redis://:123456@127.0.0.1:16379/0
```

测试连接：

```powershell
docker exec -it redis redis-cli -a "123456" ping
```

## MySQL

| 配置项 | 值 |
| --- | --- |
| 地址 | `127.0.0.1` |
| 端口 | `13306` |
| 用户名 | `root` |
| 密码 | `123456` |
| 数据库 | `pystudy` |

连接 URL：

```text
mysql://root:123456@127.0.0.1:13306/pystudy
```

测试连接：

```powershell
docker exec -it mysql mysql -uroot -p123456 pystudy
```
