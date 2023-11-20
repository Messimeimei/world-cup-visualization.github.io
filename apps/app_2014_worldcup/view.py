# coding:   utf-8
# 作者(@Author):   Messimeimei
# 创建时间(@Created_time): 2023/9/21 19:30

"""2014世界杯各个图表绘制函数"""

# 国家名称：可以重复利用
import pandas as pd
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
import os

data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/进球数据.csv')
country_name = []
country_name_chinese = [
    "德国",
    "瑞士","哥斯达黎加","阿根廷","荷兰","法国","比利时","哥伦比亚",
    "波斯尼亚",
    "尼日利亚","阿尔及利亚","美国","加纳","墨西哥","厄瓜多尔","智利",
    "希腊",
    "克罗地亚","俄罗斯","韩国","西班牙","英格兰","科特迪瓦","日本",
    "巴西",
    "伊朗","意大利","乌拉圭","葡萄牙","澳大利亚","洪都拉斯","喀麦隆",
]
a = list(data.iloc[:, 0])
for i in a :
    name = i[3:]
    country_name.append(name)

# 生成文件夹
# for i in country_name:
#     if not os.path.exists(i):
#         os.mkdir(i)


# 进攻-防守雷达图
def radar():
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Radar
    """获得每个国家的数据然后求平均值"""

    # 进球率
    path1 = r"../../data/2014_world_cup/球队进攻数据/射门数据.csv"
    path2 = r"../../data/2014_world_cup/球队进攻数据/进球数据.csv"
    shotnum = pd.read_csv(path1, usecols=["Total"]).sum().iloc[0]
    goalnum = pd.read_csv(path2, usecols=['Total']).sum().iloc[0]
    goal_rate = goalnum / shotnum

    # 传威胁球成功率
    path1 = r"../../data/2014_world_cup/球队进攻数据/传球数据.csv"
    path2 = r"../../data/2014_world_cup/球队进攻数据/关键传球数据.csv"
    dangernum = pd.read_csv(path2, usecols=["Total"]).sum().iloc[0]
    passnum = pd.read_csv(path1, usecols=["Total"]).sum().iloc[0]
    danger_rate = dangernum / passnum

    # 过人成功率
    path1 = r"../../data/2014_world_cup/球队进攻数据/过人数据.csv"
    succesnum = pd.read_csv(path1, usecols=["Successful"]).sum().iloc[0]
    totalnum = pd.read_csv(path1, usecols=["Total Dribbles"]).sum().iloc[0]
    pass_rate = succesnum / totalnum

    # 控球成功率
    path1 = r"../../data/2014_world_cup/球队进攻数据/传球数据.csv"
    acclp = pd.read_csv(path1, usecols=["AccLB"]).sum().iloc[0]
    accsp = pd.read_csv(path1, usecols=["AccSP"]).sum().iloc[0]
    passnum = pd.read_csv(path1, usecols=["Total"]).sum().iloc[0]
    control_rate = (accsp + acclp) / passnum

    # 远射能力
    path1 = r"../../data/2014_world_cup/球队进攻数据/进球数据.csv"
    outbox_goal = pd.read_csv(path1, usecols=["OutOfBox"]).sum().iloc[0]
    goalnum = pd.read_csv(path1, usecols=["Total"]).sum().iloc[0]
    outbox_rate = outbox_goal / goalnum

    # 禁区射门能力
    inside_rate = 1 - outbox_rate

    # 高空防守能力
    path1 = r"../../data/2014_world_cup/球队防守数据/高空对抗数据.csv"
    won = pd.read_csv(path1, usecols=["Won"]).sum().iloc[0]
    total = pd.read_csv(path1, usecols=["Total"]).sum().iloc[0]
    high_rate = won / total

    # 守门能力
    path1 = r"../../data/2014_world_cup/球队防守数据/扑救数据.csv"
    savenum = int(pd.read_csv(path1, usecols=["Total"]).sum().iloc[0])

    # 铲球能力
    path1 = r"../../data/2014_world_cup/球队防守数据/铲球数据.csv"
    won = pd.read_csv(path1, usecols=["TotalTackles"]).sum().iloc[0]
    total = pd.read_csv(path1, usecols=["TotalAttemptedTackles"]).sum().iloc[0]
    groun_rate = won / total

    # 射门封锁能力
    path1 = r"../../data/2014_world_cup/球队防守数据/封锁数据.csv"
    shotblock_num = int(pd.read_csv(path1, usecols=["ShotsBlocked"]).sum().iloc[0])

    # 传球封锁能力
    path1 = r"../../data/2014_world_cup/球队防守数据/封锁数据.csv"
    crossblock_num = pd.read_csv(path1, usecols=["CrossesBlocked"]).sum().iloc[0]
    passblock_num = pd.read_csv(path1, usecols=["PassesBlocked"]).sum().iloc[0]
    ballblock_num = int(crossblock_num + passblock_num)

    # 犯规次数
    path1 = r"../../data/2014_world_cup/球队防守数据/红黄牌数.csv"
    path2 = r"../../data/2014_world_cup/球队防守数据/犯规数据.csv"
    yellow = pd.read_csv(path1, usecols=["Yellow"]).sum().iloc[0]
    red = pd.read_csv(path1, usecols=["Red"]).sum().iloc[0]
    foul = pd.read_csv(path2, usecols=["Fouls"]).sum().iloc[0]
    fouls = int(yellow + red + foul)

    attack = [[goal_rate, danger_rate, pass_rate, control_rate, outbox_rate, inside_rate]]
    defence = [[savenum, high_rate, groun_rate, shotblock_num, ballblock_num, fouls]]

    c = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="进球", max_=1),
                opts.RadarIndicatorItem(name="威胁球", max_=1),
                opts.RadarIndicatorItem(name="过人", max_=1),
                opts.RadarIndicatorItem(name="控球", max_=1),
                opts.RadarIndicatorItem(name="远射", max_=1),
                opts.RadarIndicatorItem(name="终结", max_=1),
            ],
            textstyle_opts=opts.TextStyleOpts(font_size=8, font_weight='bold',color='white'),
            radius='65%'
        )

        .add("进攻能力", attack, color='#78d8ff')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                selected_mode="multiple", legend_icon="diamond", border_width=0,
                textstyle_opts=opts.TextStyleOpts(font_size=10, color='white'),
                pos_top="90%"
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
        .render("进攻雷达图.html")
    )

    d = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="守门员扑救能力", max_=500),
                opts.RadarIndicatorItem(name="高空防守", max_=1),
                opts.RadarIndicatorItem(name="地面铲球", max_=1),
                opts.RadarIndicatorItem(name="射门封堵", max_=500),
                opts.RadarIndicatorItem(name="拦截数", max_=1500),
                opts.RadarIndicatorItem(name="犯规数", max_=2500),
            ],
            textstyle_opts=opts.TextStyleOpts(font_size=8, font_weight='bold', color='white'),
            radius='60%'
        )
        .add("防守能力", defence, color="#78d8ff")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                selected_mode="multiple", legend_icon="diamond", border_width=0,
                textstyle_opts=opts.TextStyleOpts(font_size=10, color='white'),
                pos_top="90%",
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
        .render("防守雷达图.html")
    )


# 国家地图
def country_map(directory, country_name):
    from pyecharts import options as opts
    from pyecharts.charts import Map3D
    from pyecharts.globals import ChartType
    from pyecharts.commons.utils import JsCode

    c = (
        Map3D()
        .add_schema(
            box_height=100,
            box_depth=80,
            maptype=f'{country_name}',
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgb(5,101,123)",
                opacity=1,
                border_width=0.8,
                border_color="rgb(62,215,213)",
            ),
            map3d_label=opts.Map3DLabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + " " + data.value[2];}"),
            ),
            emphasis_label_opts=opts.LabelOpts(
                is_show=False,
                color="#fff",
                font_size=10,
                background_color="rgba(0,23,11,0)",
            ),
            light_opts=opts.Map3DLightOpts(
                main_color="#fff",
                main_intensity=1.2,
                main_shadow_quality="high",
                is_main_shadow=False,
                main_beta=10,
                ambient_intensity=0.3,
            ),
        )

        .add(

            series_name = '',
            data_pair = '',
            type_=ChartType.MAP3D,
            shading="lambert",
            label_opts=opts.LabelOpts(
                is_show=False,
                formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
            ),
        )

        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
        )


        .render(f"./{directory}/{country_name}地图.html")
    )


# 进球分析图
def goal_analyse(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Pie

    # 读取数据
    data = pd.read_csv("../../data/2014_world_cup/球队进攻数据/进球数据.csv")
    data = data.iloc[number, :]
    sixyardbox = int(data[2])    # 大禁区内
    PenaltyArea = int(data[3])   # 小禁区内
    OutOfBox = int(data[4])      # 禁区外
    c = (
        Pie()
        .add(
            "进球来源占比", [["大禁区内进球",sixyardbox], ['小禁区内进球',PenaltyArea], ['禁区外进球',OutOfBox]],
            radius="50%"

        )
        .set_colors(["#326bab", "#78d8ff", "#0766ff"])
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_top="10%", border_width=0,
                textstyle_opts=opts.TextStyleOpts(color='white')
            ),

        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),

        )
        .render(f"./{directory}/{country}进球分析-饼图.html")
    )


# 传球成功率水滴图
def pass_rate(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Grid, Liquid
    from pyecharts.commons.utils import JsCode

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/传球数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    AccLB = int(data[2])
    InAccLB = int(data[3])
    AccSP = int(data[4])
    InAccSP = int(data[5])

    pass_rate = (AccLB + AccSP) / Total # 传球成功率
    lb_rate = AccLB / Total # 长传成功率
    sb_rate = AccSP / Total # 短传成功率

    l1 = (
        Liquid()
        .add(
            "传球成功率", [pass_rate], center=["50%", "40%"],
            label_opts=opts.LabelOpts(
                font_size=10,
                formatter=JsCode(
                    """function (param) {
                            return (Math.floor(param.value * 10000) / 100) + '%';
                        }"""
                ),
                position="inside",
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(
            title="传球数据分析", pos_top="20", pos_left="5%"),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )

    l2 = Liquid().add(
        "长传成功率",
        [lb_rate],
        center=["20%", "60%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
            ),
            position="inside",
        ),
    )

    l3 = Liquid().add(
        "短传成功率",
        [sb_rate],
        center=["80%", "60%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
            ),
            position="inside",
        ),
    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts()).add(l3, grid_opts=opts.GridOpts())
    grid.render(f"./{directory}/{country}传球成功率分析-水滴图.html")


# 传威胁球仪表盘图
def key_pass(directory, number, country):
    import pandas as pd
    import pyecharts.options as opts
    from pyecharts.charts import Gauge

    data =  pd.read_csv('../../data/2014_world_cup/球队进攻数据/关键传球数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    Long = int(data[2])
    Short = int(data[3])

    (
        Gauge()
        .add(
            series_name="", data_pair=[["总威胁球数", Total]],
            title_label_opts=opts.GaugeTitleOpts(offset_center=["0%", "20%"], color='white'),
            detail_label_opts=opts.GaugeDetailOpts(formatter="{value}", offset_center=["0%", "40%"],color='white'),
            progress=opts.GaugeProgressOpts(is_show=False),  # 显示最外层的进度
            axislabel_opts=opts.LabelOpts(color='#a1cadf'),    # 修改刻度文字颜色
            axistick_opts=opts.AxisTickOpts(
                linestyle_opts=opts.LineStyleOpts(color='white')
            ),  # 修改刻度颜色
            pointer=opts.GaugePointerOpts(length='70%'),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True),

        )
        .set_series_opts(
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[[(Long/100), "#3a5578"], [(Short/100), "#37a2da"], [1, "#2e3756"]], width=30
                )
            )
        )
        .render(f"./{directory}/{country}威胁球分析-仪表盘图.html")
    )


# 传球柱状图数据
def pass_bar(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.globals import ThemeType

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/传球数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    AccLB = int(data[2])
    InAccLB = int(data[3])
    AccSP = int(data[4])
    InAccSP = int(data[5])


    list1 = [
        {"value": AccSP, "percent":  AccSP / (AccSP + InAccSP)},
        {"value": AccLB, "percent": AccLB / (AccLB + InAccLB)},
    ]
    list2 = [
        {"value": InAccSP, "percent": InAccSP / (AccSP + InAccSP)},
        {"value": InAccLB, "percent": InAccLB / (AccLB + InAccLB)},
    ]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="500px", height="500px"))
        .add_xaxis(["短传球", "长传球"])
        .add_yaxis(
            "成功数", list1, stack="stack1", category_gap="30%", color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7")
        )
        .add_yaxis(
            "失败数", list2, stack="stack1", category_gap="30%", color='#a1cadf', gap="20%", bar_width=40,
            itemstyle_opts=opts.ItemStyleOpts(color="#001e55"),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .render(f"./{directory}/{country}传球分析-柱状图.html")
    )


# 过人柱状图数据
def dribble(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.globals import ThemeType

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/过人数据.csv')
    data = data.iloc[number, :]
    Total = int(data[3])
    success = int(data[2])
    unsuccess = int(data[1])


    y = [success, unsuccess, Total]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="500px", height="500px"))
        .add_xaxis(["成功过人数", "失败过人数", "总过人数"])
        .add_yaxis(
            "过人数据", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7")
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .render(f"./{directory}/{country}过人分析-柱状图.html")
    )


# 射门数据
def shoot(directory, number, country):
    import pandas as pd
    import pyecharts.options as opts
    from pyecharts.charts import Pie
    from pyecharts.charts import Bar
    from pyecharts.globals import ThemeType
    from pyecharts.charts import Grid


    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/射门数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    OutOfBox = int(data[2])
    SixYardBox = int(data[3])
    PenaltyArea = int(data[4])

    x_data = ["小禁区射门", "大禁区射门", "禁区外射门"]
    y_data = [SixYardBox, PenaltyArea, OutOfBox]
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    p = (
         Pie()
        .add(
            series_name="射门数据",
            data_pair=data_pair,
            rosetype="radius",
            radius="20%",
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
        )
     )

    y = [OutOfBox, SixYardBox, PenaltyArea, Total]

    c = (
        Bar(init_opts=opts.InitOpts(width="300px", height="300px"))
        .add_xaxis(["禁区外射门", "小禁区内射门", "大禁区内射门", "总射门数"])
        .add_yaxis(
            "过人数据", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7", border_width=20)
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
    )

    grid = Grid(init_opts=opts.InitOpts(width="500px", height="500px"))
    grid.add(c, opts.global_options.GridOpts(pos_left="60%"))
    grid.add(p, opts.global_options.GridOpts(pos_right="50%"))

    grid.render(f"./{directory}/{country}射门分析-玫瑰图.html")


# 过人成功率
def dribble_rate(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Liquid
    from pyecharts.globals import SymbolType

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/过人数据.csv')
    data = data.iloc[number, :]
    Total = int(data[3])
    success = int(data[2])
    unsuccess = int(data[1])

    c = (
        Liquid()
        .add("过人成功率", [success / Total], is_outline_show=False, shape=SymbolType.DIAMOND)
        .render(f"./{directory}/{country}过人成功率分析-水滴图.html")
    )


# 射门转化率
def control_ball(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Liquid
    from pyecharts.globals import SymbolType

    shoot_data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/射门数据.csv')
    goal_data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/进球数据.csv')
    shoot_data = shoot_data.iloc[number, :]
    shoot_Total = int(shoot_data[1])
    goal_data = goal_data.iloc[0, :]
    goal_Total = int(goal_data[1])

    rate = goal_Total / shoot_Total

    c = (
        Liquid()
        .add("射门转化率", [rate], is_outline_show=False, shape=SymbolType.DIAMOND)
        .render(f"./{directory}/{country}射门转化率分析-水滴图.html")
    )


# 高空对抗柱状图
def high_battle(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.globals import ThemeType

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/高空对抗数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    won = int(data[2])
    lost = int(data[3])

    y = [won, lost, Total]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="500px", height="500px"))
        .add_xaxis(["成功对抗数", "失败对抗数", "总对抗数"])
        .add_yaxis(
            "高空对抗数据", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7")
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .render(f"./{directory}/{country}高空对抗分析-柱状图.html")
    )


# 高空对抗成功率
def high_battle_rate(directory, number, country):
    import pandas as pd
    from pyecharts.charts import Liquid
    from pyecharts.globals import SymbolType

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/高空对抗数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    won = int(data[2])
    lost = int(data[3])

    c = (
        Liquid()
        .add("过人成功率", [won / Total], is_outline_show=False, shape=SymbolType.DIAMOND)
        .render(f"./{directory}/{country}高空对抗成功率分析-水滴图.html")
    )


# 铲球柱状图
def tackle(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.globals import ThemeType

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/铲球数据.csv')
    data = data.iloc[number, :]
    Total = int(data[3])
    won = int(data[1])
    lost = int(data[2])

    y = [won, lost, Total]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="500px", height="500px"))
        .add_xaxis(["成功铲球数", "失败铲球数", "总铲球数"])
        .add_yaxis(
            "铲球数据", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7")
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .render(f"./{directory}/{country}铲球分析-柱状图.html")
    )


# 铲球成功率
def tackle_rate(directory, number, country):
    import pandas as pd
    from pyecharts.charts import Liquid
    from pyecharts.globals import SymbolType

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/铲球数据.csv')
    data = data.iloc[number, :]
    Total = int(data[3])
    won = int(data[1])
    lost = int(data[2])

    c = (
        Liquid()
        .add("铲球成功率", [won / Total], is_outline_show=False, shape=SymbolType.DIAMOND)
        .render(f"./{directory}/{country}铲球成功率分析-水滴图.html")
    )


# 扑救数据
def save(directory, number, country):
    import pandas as pd
    import pyecharts.options as opts
    from pyecharts.charts import Pie
    from pyecharts.charts import Bar
    from pyecharts.charts import Grid

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/扑救数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])
    OutOfBox = int(data[4])
    SixYardBox = int(data[2])
    PenaltyArea = int(data[3])

    x_data = ["小禁区扑救", "大禁区扑救", "远射扑救"]
    y_data = [SixYardBox, PenaltyArea, OutOfBox]
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])

    p = (
        Pie()
        .add(
            series_name="扑救数据",
            data_pair=data_pair,
            rosetype="radius",
            radius="20%",
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                pos_left="center",
                pos_top="20",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)"),
        )
    )

    y = [OutOfBox, SixYardBox, PenaltyArea, Total]

    c = (
        Bar(init_opts=opts.InitOpts(width="300px", height="300px"))
        .add_xaxis(["远射扑救", "小禁区内扑救", "大禁区内扑救", "总扑救数"])
        .add_yaxis(
            "扑救数据", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7", border_width=20)
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
    )

    grid = Grid(init_opts=opts.InitOpts(width="500px", height="500px"))
    grid.add(c, opts.global_options.GridOpts(pos_left="60%"))
    grid.add(p, opts.global_options.GridOpts(pos_right="50%"))

    grid.render(f"./{directory}/{country}扑救分析-饼图.html")


# 拦截数据
def interception(directory, number, country):
    import pandas as pd
    import pyecharts.options as opts
    from pyecharts.charts import Gauge

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/拦截数据.csv')
    data = data.iloc[number, :]
    Total = int(data[1])

    (
        Gauge()
        .add(
            series_name="", data_pair=[["拦截数", Total]],
            title_label_opts=opts.GaugeTitleOpts(offset_center=["0%", "20%"], color='white'),
            detail_label_opts=opts.GaugeDetailOpts(formatter="{value}", offset_center=["0%", "40%"], color='white'),
            progress=opts.GaugeProgressOpts(is_show=False),  # 显示最外层的进度
            axislabel_opts=opts.LabelOpts(color='#a1cadf'),  # 修改刻度文字颜色
            axistick_opts=opts.AxisTickOpts(
                linestyle_opts=opts.LineStyleOpts(color='white')
            ),  # 修改刻度颜色
            pointer=opts.GaugePointerOpts(length='70%'),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True),

        )
        .set_series_opts(
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[[(Total / 100), "#3a5578"], [1, "#2e3756"]], width=30
                )
            )
        )
        .render(f"./{directory}/{country}拦截分析-仪表盘图.html")
    )


# 封锁数据
def block(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Pie

    # 读取数据
    data = pd.read_csv("../../data/2014_world_cup/球队防守数据/封锁数据.csv")
    data = data.iloc[number, :]
    ShotsBlocked = int(data[1])    # 大禁区内
    CrossesBlocked = int(data[2])   # 小禁区内
    PassesBlocked = int(data[3])      # 禁区外
    c = (
        Pie()
        .add(
            "封堵占比", [["封堵射门",ShotsBlocked], ['封堵传中',CrossesBlocked], ['封堵传球',PassesBlocked]],
            radius="50%"

        )
        .set_colors(["#326bab", "#78d8ff", "#0766ff"])
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top="10%", border_width=0,
                textstyle_opts=opts.TextStyleOpts(
                    color="white"
                ), item_gap=20
            ),

        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),

        )
        .render(f"./{directory}/{country}封堵分析-饼图.html")
    )


# 红黄牌数
def red_yellow_card(directory, number, country):
    import pandas as pd
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    from pyecharts.globals import ThemeType

    data = pd.read_csv('../../data/2014_world_cup/球队防守数据/红黄牌数.csv')
    data = data.iloc[number, :]
    yellow = int(data[1])
    red = int(data[2])
    total = yellow + red


    y = [yellow, red, total]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="500px", height="500px"))
        .add_xaxis(["黄牌数", "红牌数", "总得牌数"])
        .add_yaxis(
            "红黄牌数", y, color='#a1cadf', gap="20%",
            itemstyle_opts=opts.ItemStyleOpts(color="#3068a7")
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#a1cadf"
            ),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .render(f"./{directory}/{country}红黄牌数分析-柱状图.html")
    )


# 整体-国家队进球分析
def whole_goal():
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    import pandas as pd

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/进球数据.csv')
    data = list(data['Total'])
    print(data)


    c = (
        Bar(
            init_opts=opts.InitOpts(
                bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat" , "position":"center"}
            )
        )
        .add_xaxis(country_name)
        .add_yaxis("进球数", data, color=Faker.rand_color(), is_realtime_sort=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="各国家队总进球数比较", title_textstyle_opts=opts.TextStyleOpts(color='white')
            ),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
            legend_opts=opts.LegendOpts(border_width=0, textstyle_opts=opts.TextStyleOpts(color="white")),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "color": JsCode(
                        """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""
                    ),
                    "barBorderRadius": [20, 20, 20, 20],
                    "shadowColor": "rgb(0, 160, 221)",
                }
            }
        )
    )
    c.add_js_funcs(
        """
        var img = new Image(); img.src = '../static/images/整体进球对比背景图.png';
        """
    )
    c.render("各国家队总进球数比较.html")


# 整体-进球类型分析
def whole_goal_type():
    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker
    import pandas as pd

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/进球数据.csv')
    SixYardBox = int(data['SixYardBox'].sum())
    PenaltyArea = int(data['PenaltyArea'].sum())
    OutOfBox = int(data['OutOfBox'].sum())



    c = (
        Pie()
        .add("", [("小禁区进球", SixYardBox), ("大禁区进球", PenaltyArea), ('远射进球', OutOfBox)])
        .set_colors(["#2b435f", "#056c84", "#1452ef"])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="进球占比", title_textstyle_opts=opts.TextStyleOpts(color='black')),
            legend_opts=opts.LegendOpts(border_width=0, textstyle_opts=opts.TextStyleOpts(color='black'))
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("总进球占比分析.html")
    )


# 整体-国家队传球次数
def whole_pass():
    from pyecharts import options as opts
    from pyecharts.charts import PictorialBar
    from pyecharts.globals import SymbolType

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/传球数据.csv')
    total = list(data['Total'])

    c = (
        PictorialBar()
        .add_xaxis(country_name)
        .add_yaxis(
            "",
            total,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=9,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol='circle',
            color='#78d8ff'
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="国家队传球数据", title_textstyle_opts=opts.TextStyleOpts(color='black')),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='black'), is_show=False)
        )
        .render("国家队总传球数.html")
    )


# 整体-国家队过人分析
def whole_dribble():
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    import pandas as pd

    data = pd.read_csv('../../data/2014_world_cup/球队进攻数据/过人数据.csv')
    data = list(data['Total Dribbles'])
    print(data)


    c = (
        Bar(
            init_opts=opts.InitOpts(
                bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat" , "position":"center"}
            )
        )
        .add_xaxis(country_name)
        .add_yaxis("过人数", data, color=Faker.rand_color(), is_realtime_sort=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="各国家队总过人数比较", title_textstyle_opts=opts.TextStyleOpts(color='white')
            ),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
            legend_opts=opts.LegendOpts(border_width=0, textstyle_opts=opts.TextStyleOpts(color="white")),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False))
        )
        .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "color": JsCode(
                        """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""
                    ),
                    "barBorderRadius": [20, 20, 20, 20],
                    "shadowColor": "rgb(0, 160, 221)",
                }
            }
        )
    )
    c.add_js_funcs(
        """
        var img = new Image(); img.src = '../static/images/整体过人对比背景图.png';
        """
    )
    c.render("各国家队过人数比较.html")


if __name__ == '__main__':
    for i in range(len(country_name)):
        country_map(country_name[i], country_name_chinese[i] )  # 统一生成地图
        goal_analyse(country_name[i], i, country_name_chinese[i])   # 统一生成进球分析图
        pass_rate(country_name[i], i, country_name_chinese[i])  # 统一生成传球成功率图
        key_pass(country_name[i], i, country_name_chinese[i])  # 统一生成威胁球分析图
        pass_bar(country_name[i], i, country_name_chinese[i])  # 统一生成传球分析图
        dribble(country_name[i], i, country_name_chinese[i])  # 统一生成过人分析图
        shoot(country_name[i], i, country_name_chinese[i])  # 统一生成射门分析图
        dribble_rate(country_name[i], i, country_name_chinese[i])   # 统一生成过人成功率分析图
        control_ball(country_name[i], i, country_name_chinese[i])   # 统一生成射门转化率分析图
        high_battle(country_name[i], i, country_name_chinese[i])  # 统一生成高空对抗分析图
        high_battle_rate(country_name[i], i, country_name_chinese[i])  # 统一生成高空对抗成功率分析图
        tackle(country_name[i], i, country_name_chinese[i])  # 统一生成铲球分析图
        tackle_rate(country_name[i], i, country_name_chinese[i])  # 统一生成铲球成功率分析图
        save(country_name[i], i, country_name_chinese[i])  # 统一生成扑救分析图
        interception(country_name[i], i, country_name_chinese[i])  # 统一生成拦截分析图
        block(country_name[i], i, country_name_chinese[i])  # 统一生成封堵分析图
        red_yellow_card(country_name[i], i, country_name_chinese[i])  # 统一生成红黄牌数分析图
