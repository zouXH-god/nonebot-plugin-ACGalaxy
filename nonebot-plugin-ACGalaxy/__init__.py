from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from . import acg


__plugin_meta__ = PluginMetadata(
    name="次元星辰",
    description="简单好用的漫展信息展示插件，收集展示漫展信息，支持检索、排序、获取定位信息",
    usage="发送 '漫展日历 城市' | '漫展位置 漫展id' | '漫展信息 漫展id' | '漫展检索 关键词' 获取对应信息",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
    ),
    homepage="https://github.com/zouXH-god/nonebot-plugin-ACGalaxy",
    # 发布必填。
)