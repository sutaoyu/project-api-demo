[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# 介绍

- 后端框架模板
    - 语言：python 
    - 后端框架：`Fastapi`
    - 后端数据库：`Mysql`
    - 检索数据库：`ElastiSearch`


# 使用方法
1. 复制环境“clone项目至本地，修改项目名称
2. 环境配置：进行python环境配置，参考后续**环境配置**章节
3. 开发环境配置：在`project-api-demo/app/core/config.py`中配置开发环境变量，如`Mysql`和`ElastiSearch`数据库连接地址，如果没有`Mysql`和`ElastiSearch`服务，则需要提前安装
4. 数据导入：为了快速开始后端接口使用，可以在`Mysql`数据库运行`project-api-demo/sql/readme.md`中sql语句，创建对应的数据库和表
5. 接口书写：书写针对`Mysql`数据库的CRUD，可参考后续**CRUD基本步骤**章节，针对`ElastiSearch`数据库的查询，可以参考`project-api-demo/app/api/api_v1/endpoints/search.py`
6. 调试程序：参考后续**程序运行**章节
7. 书写测试样例：参考后续**Pytest 测试举例**章节
8. 提交git仓库：参考后续**Commit提交规范**和**Git使用**章节
9. 部署程序：参考后续**程序运行**章节


# 环境配置

```
conda create -n project-api-demo python=3.9

conda activate project-api-demo

pip install -r requirements.txt

```

# CRUD基本步骤

1. 创建数据库模型（`models/xxx.py`）

- 在`models/__init__.py`中引入相应的类 (依据根目录下table.sql创建)

2. 创建 Pydantic 模型 (`schemas/xxx.py`)

- 在`schemas/__init__.py`中引入相应的类

3. 创建CRUD基本操作 (`crud/crud_xxx.py`)

- 在`crud/__init__.py`中引入相应的类

4. 编写接口 (`api/api_v1/endpoints/xxx.py`)

- 在`api/api_v1/api.py`中加入对应的`api_router`

5. 接口规范与此[参考](https://github.com/sutaoyu/Let-us-warm-up/blob/main/api.md)保持统一

# 程序运行

- 激活环境

```
conda activate project-api-demo
```

- 调试程序（debug 8107端口、单线程）

```
bash debug_app.sh
```

- 后台启动程序 (run 8106端口、多线程)

```
bash run_app.sh
```

- 关闭后台程序 (stop)

```
bash stop_app.sh
```

# Git使用

- Merge Request 分支合并请求 [参考](https://juejin.cn/post/7028965736022278175)


# Pytest 测试举例


- 测试test_users.py所有用例

```
pytest -v -s test_users.py
```

- 测试test_users.py里面的`test_get_existing_user`方法

```
pytest -v -s test_users.py::test_get_existing_user
```


# Commit提交规范
- 参考[如何写commit](https://blog.csdn.net/zyx6a/article/details/129908204)

- feat： 一个新的功能（feature）；
- fix：修复bug;
- docs：修改文档，比如README.md、CHANGELOG.md等；
- style:    修改代码的格式，不影响代码运行的变动，比如空格、格式化代码、补齐句末分号等等；
- refactor:   代码的重构，没有新功能的添加以及bug修复的代码改动；
- perf：优化代码以提高性能；
- test：增加测试或优化改善现有的测试；
- build：修改影响项目构建文件或外部依赖项，比如npm、gulp、webpack、broccoli等；
- ci：修改CI配置文件和脚本；
- chore：其他非src路径文件和测试文件的修改，比如.gitignore、.editorconfig等；
- revert：代码回退；


# 参考项目

- 官方项目[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- Black Formatter 代码格式化工具 [官方](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) [说明](https://muzing.top/posts/a29e4743/#the-black-code-style)
- fastapi 数据库使用 [sql-databases](https://fastapi.tiangolo.com/zh/tutorial/sql-databases/)
- fastapi 权限认证 [security](https://fastapi.tiangolo.com/zh/tutorial/security/)
- fastapi+celery的初步使用 [参考](https://derlin.github.io/introduction-to-fastapi-and-celery/03-celery/)
- fastapi+celery的高阶使用 [参考](https://www.fastapitutorial.com/blog/introduction-to-task-queue/)
- celery 官方文档 [参考](https://celeryproject.readthedocs.io/zh_CN/latest/index.html#)
- celery 中文手册 [参考](https://www.celerycn.io/)
- celry 守护进程 [参考](https://blog.csdn.net/weixin_43064185/article/details/96479241)
- pytest的初步使用 [参考](https://www.cnblogs.com/hiyong/tag/pytest/)
- pytest中新插入的数据无法获取的问题 [解释](https://www.cnblogs.com/wintest/p/12825371.html)、[SqlAlchemy](https://www.cnblogs.com/huchong/p/9258458.html)、[解决方案](https://blog.csdn.net/wenxingchen/article/details/129069617)
