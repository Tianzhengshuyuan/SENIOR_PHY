1. 构建数据库phy_senior.sql，使用下面的命令：
```bash
./generate_sql.sh
```

2. 运行数据库
```bash
sudo mysql < sql/phy_senior.sql
```

3. 查询数据库
```bash
python query_sql.py 
``` 