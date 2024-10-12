import json
import os
import time

from arclet.alconna import Alconna, Args
from nonebot import get_driver
from nonebot_plugin_alconna import UniMessage, on_alconna, AlconnaMatcher
from .utils import get_acg_list, get_acg_info, capture_element_screenshot, get_coordinate_url, get_guest_list, \
    get_guest_acg_list

driver = get_driver()
acg_calendar = on_alconna(
    Alconna("漫展日历", Args["city?", str]),
    aliases={"日历", "展会日历"},
    block=True,
    priority=11,
)
acg_coordinate = on_alconna(
    Alconna("漫展位置", Args["acgId?", str]),
    aliases={"位置信息", "位置"},
    block=True,
    priority=11,
)
acg_info = on_alconna(Alconna(
    "漫展详情", Args["acgId?", str]),
    aliases={"展会详情", "漫展信息", "展会详情"},
    block=True,
    priority=11,
)
acg_search = on_alconna(
    Alconna("漫展检索", Args["key?", str]),
    aliases={"展会检索", "检索", "漫展查询"},
    block=True,
    priority=11,
)
acg_guest = on_alconna(
    Alconna("嘉宾检索", Args["guest?", str]),
    aliases={"嘉宾查询", "嘉宾搜索", "查询嘉宾"},
    block=True,
    priority=11,
)

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)


@acg_calendar.handle()
async def acg_calendar_h(matcher: AlconnaMatcher, city: str):
    matcher.set_path_arg("city", city)

@acg_calendar.got_path("city", prompt="请输入城市")
async def acg_calendar_g(city: str):
    acg_list = await get_acg_list(city_name=city, count=100, order="time")
    # print(acg_list)
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
    with open(os.path.join(script_directory, "templates/acg_list.html"), "r", encoding="utf-8") as fp:
        html_content = fp.read().replace("@@acg_list@@", json.dumps(acg_list.get("data")))
    img_data = await capture_element_screenshot(html_content)
    await acg_search.finish(msg + UniMessage.image(raw=img_data))
    

@acg_guest.handle()
async def acg_guest_h(matcher: AlconnaMatcher, guest: str):
    matcher.set_path_arg("guest", guest)
    

@acg_guest.got_path("guest", prompt="请输入嘉宾CN")
async def acg_guest_g(guest: str):
    guest_list = await get_guest_list(guest)
    guest_acg_list = []
    if len(guest_list) == 0:
        acg_guest.finish("未找到相关嘉宾信息")
        return
    for guest in guest_list:
        guest_acg = await get_guest_acg_list(guest.get("id"))
        guest_acg_list += guest_acg
    msg = f"找到相关嘉宾 {len(guest_list)} 条\n找到相关漫展 {len(guest_acg_list)} 条\n"
    with open(os.path.join(script_directory, "templates/acg_list_guest.html"), "r", encoding="utf-8") as fp:
        html_content = fp.read().replace("@@acg_list@@", json.dumps(guest_acg_list)).replace("@@guest_list@@",
                                                                                           json.dumps(guest_list))
    img_data = await capture_element_screenshot(html_content)
    await acg_search.finish(msg + UniMessage.image(raw=img_data))
    