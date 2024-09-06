import json
import os
import time

from arclet.alconna import Alconna, Args
from nonebot import get_driver
from nonebot_plugin_alconna import UniMessage, on_alconna, AlconnaMatcher
from .utils import get_acg_list, get_acg_info, capture_element_screenshot, get_coordinate_url

driver = get_driver()
acg_calendar = on_alconna(Alconna("漫展日历", Args["city?", str]))
acg_coordinate = on_alconna(Alconna("漫展位置", Args["acgId?", str]))
acg_info = on_alconna(Alconna("漫展详情", Args["acgId?", str]))
acg_search = on_alconna(Alconna("漫展检索", Args["key?", str]))


@acg_calendar.handle()
async def acg_calendar_h(matcher: AlconnaMatcher, city: str):
    matcher.set_path_arg("city", city)

@acg_calendar.got_path("city", prompt="请输入城市")
async def acg_calendar_g(city: str):
    acg_list = await get_acg_list(city_name=city, count=100, order="time")
    print(acg_list)
    start_time = ""
    acg_data = {}
    for acg in acg_list.get("data"):
        if acg.get("start_unix") <= time.time():
            acg["start_time"] = "进行中"
        if start_time != acg.get("start_time"):
            start_time = acg.get("start_time")
            acg_data[start_time] = []
        acg_data[start_time].append(acg)
    if not acg_data:
        acg_calendar.finish("未找到相关漫展信息")
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    with open(os.path.join(script_directory, "templates/acg_list_times.html"), "r", encoding="utf-8") as fp:
        html_content = fp.read().replace("@@acg_list@@", json.dumps(acg_data))
    img_data = await capture_element_screenshot(html_content)
    await acg_calendar.send(UniMessage.image(raw=img_data))


@acg_coordinate.handle()
async def acg_coordinate_h(matcher: AlconnaMatcher, acgId: str):
    matcher.set_path_arg("acgId", acgId)


@acg_coordinate.got_path("acgId", prompt="请输入漫展id")
async def acg_coordinate_g(acgId: str):
    acg_info = await get_acg_info(acgId)
    msg = ""
    msg += f"漫展名称：{acg_info.get('project_name')}\n"
    msg += f"漫展地点：{acg_info.get('venue_name')}\n"
    msg += f"漫展位置：{get_coordinate_url(acg_info.get('coordinate'))}\n"
    await acg_coordinate.finish(msg)


@acg_info.handle()
async def acg_info_h(matcher: AlconnaMatcher, acgId: str):
    matcher.set_path_arg("acgId", acgId)


@acg_info.got_path("acgId", prompt="请输入漫展id")
async def acg_info_g(acgId: str):
    acg_info = await get_acg_info(acgId)
    cover = UniMessage.image(url=acg_info.get("cover"))
    msg = "".join([
        f"漫展id：{acg_info.get('id')}\n",
        f"漫展名称：{acg_info.get('project_name')}\n",
        f"漫展地点：{acg_info.get('venue_name')}\n",
        f"漫展时间：{acg_info.get('start_time')} - {acg_info.get('end_time')}\n",
        f"展票价格：{acg_info.get('min_price') / 100} - {acg_info.get('max_price') / 100} 元\n",
        f"是否有NPC招募信息：{'是' if acg_info.get('has_npc') == 1 else '否'}\n",
        f"展会链接：\nhttps://show.bilibili.com/platform/detail.html?id={acg_info.get('id')}\n"
    ])
    await acg_coordinate.finish(cover + msg)

@acg_search.handle()
async def acg_search_h(matcher: AlconnaMatcher, key: str):
    matcher.set_path_arg("key", key)

@acg_search.got_path("key", prompt="请输入关键字")
async def acg_search_g(key: str):
    acg_list = await get_acg_list(key=key, count=100)
    if acg_list.get("count") == 0:
        acg_search.finish("未找到相关漫展信息")
    msg = f"找到结果 {acg_list.get('count')} 条\n"
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    with open(os.path.join(script_directory, "templates/acg_list.html"), "r", encoding="utf-8") as fp:
        html_content = fp.read().replace("@@acg_list@@", json.dumps(acg_list.get("data")))
    img_data = await capture_element_screenshot(html_content)
    await acg_search.finish(msg + UniMessage.image(raw=img_data))