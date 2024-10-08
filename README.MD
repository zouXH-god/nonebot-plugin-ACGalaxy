
# nonebot-plugin-ACGalaxy

_✨ 简单高效的漫展信息展示插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/commit-activity/w/zouXH-god/nonebot-plugin-ACGalaxy" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ACGalaxy">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ACGalaxy.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">


简单高效的漫展信息展示插件，收集展示漫展信息，支持检索、排序、获取定位信息

## 📖 介绍

简单高效的漫展信息展示插件，收集展示漫展信息，支持检索、排序、获取定位信息

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ACGalaxy

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ACGalaxy
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-ACGalaxy
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-ACGalaxy
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-ACGalaxy
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ACGalaxy"]

</details>

## 🎉 使用
### 指令表
|    指令     | 权限 | 需要@ | 范围 |         说明         |
|:---------:|:----:|:----:|:--:|:------------------:|
|  漫展日历 城市  | 群员 | 否 | 全部 | 获取指定城市的漫展列表（按日期排序） |
| 漫展位置 漫展id | 群员 | 否 | 全部 |    获取指定漫展的位置信息     |
| 漫展详情 漫展id | 群员 | 否 | 全部 |    获取指定漫展的详细信息     |
| 漫展检索 关键词  | 群员 | 否 | 全部 |       检索漫展信息       |
### 效果图
<div align="center">
<img src="docs/1.png"  width="50%">
</div>