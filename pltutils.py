from matplotlib import pyplot as plt
from enum import Enum
"""
Author: Eurka
Version: 0.2.0
ChangeLogs:
    2023-04-10 v0.2.3 精简代码
    2023-03-30 v0.2.2 新增绘制标记点的功能
    2023-03-30 v0.2.1 支持一次绘制多条辅助线
    2023-03-21 v0.2.0 新增绘图配色方案加载
    2022-10-24 v0.1.0 新增快速绘制 plot 图例和标识的功能
"""


class Style(Enum):
    SETE = 0
    NILOU = 1
    HUTAO = 2
    RAIDEN = 3
    N = 4


def plt_style_init(style=Style.SETE):
    """设置 matplotlib.pyplot 的全局绘图参数
    """
    # === 设置matplotlib对中文的支持 ===
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    # === 设置绘图的字体大小 ===
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["figure.figsize"] = "8, 6"
    # === 设置绘图的配色 ===
    if style == Style.SETE:
        # 青 品红 橙 黄 紫 蓝 棕
        plt.rcParams[
            "axes.prop_cycle"] = "cycler('color', ['1fa89d','e72d5c','ff7800','fabb0b','9832c3','4a57a4','a77c4f'])"
    elif style == Style.NILOU:
        plt.rcParams[
            "axes.prop_cycle"] = "cycler('color', ['#15365e','#76a1b9','#bed9e5','#65588a','#d75038'])"
    elif style == Style.HUTAO:
        plt.rcParams[
            "axes.prop_cycle"] = "cycler('color', ['#65588a','#c94737','#3a1b19','#7b595e','#c7a085'])"
    elif style == Style.RAIDEN:
        plt.rcParams[
            "axes.prop_cycle"] = "cycler('color', ['#352660','#553b93','#9772ca','#f5e7ec','#60203c'])"
    elif style == Style.N:
        plt.rcParams[
            "axes.prop_cycle"] = "cycler('color', ['#352660','#6e0f6c','#9772ca','#f5e7ec','#60203c'])"
    # === 设置绘图的图例位置 ===
    plt.rcParams["legend.loc"] = "upper right"


def post2d(ans: str,
           vars: str | tuple[str, str],
           params: dict = None,
           hasLabel=True):
    """辅助生成标准格式的 pyplot 2d绘图标注，支持Latex数学表达式

    Parameters
    ----------
    ans : str
        函数值名称
    vars : str | tuple[str, str]
        变量名称
    params : dict, optional
        参数名称, by default None
    hasLabel : bool, optional
        是否绘制图例, by default True
    
    e.g.
    ----------
    post2d("y_i", ["x", r"y_{idx}"], {"idx": "1,2,3,4,5"})
        y_i vs (x, y_idx) when idx=1,2,3,4,5
    """
    if isinstance(vars, str):
        title = f"${ans}$ vs ${vars}$"
        plt.xlabel(f"${vars}$")
        plt.ylabel(f"${ans}$")
    else:
        title = f"${ans}$ vs (${vars[0]},~{vars[1]}$)"
        plt.xlabel(f"${vars[0]}$")
        plt.ylabel(f"${vars[1]}$")
    if params is not None:
        params_str = ",~".join([f"{k}={v}" for (k, v) in params.items()])
        title += f" when ${params_str}$"
    plt.title(title)
    if hasLabel:
        plt.legend()


def line(x1y1: tuple[float, float],
         x2y2: tuple[float, float],
         color="black",
         style="--"):
    """在 pyplot.plot 中绘制辅助线

    Parameters
    ----------
    x1y1 : tuple[float, float]
        起点
    x2y2 : tuple[float, float]
        终点
    color : str, optional
        辅助线颜色, by default "black"
    style : str, optional
        辅助线样式, by default "--"
    """
    x_arr = [x1y1[0], x2y2[0]]
    y_arr = [x1y1[-1], x2y2[-1]]
    plt.plot(x_arr, y_arr, c=color, ls=style)


def line_vertical(x: float | list[float], color="black", style="--"):
    """在 pyplot.plot 中绘制垂直辅助线
    
    Notice
    ----------
    必须在 plot 之后调用

    Parameters
    ----------
    x : float | list[float]
        辅助线位置
    color : str, optional
        辅助线颜色, by default "black"
    style : str, optional
        辅助线样式, by default "--"
    """
    y_arr = plt.ylim()
    if isinstance(x, list):
        for xi in x:
            plt.plot([xi] * 2, y_arr, c=color, ls=style)
    else:
        plt.plot([x] * 2, y_arr, c=color, ls=style)
    # 避免y轴方向坐标轴扩展
    plt.ylim(y_arr)


def line_horizontal(y: float | list[float], color="black", style="--"):
    """在 pyplot.plot 中绘制水平辅助线
    
    Notice
    ----------
    必须在 plot 之后调用
    
    Parameters
    ----------
    y : float | list[float]
        辅助线位置
    color : str, optional
        辅助线颜色, by default "black"
    style : str, optional
        辅助线样式, by default "--"
    """
    x_arr = plt.xlim()
    if isinstance(y, list):
        for yi in y:
            plt.plot(x_arr, [yi] * 2, c=color, ls=style)
    else:
        plt.plot(x_arr, [y] * 2, c=color, ls=style)
    # 避免x轴方向坐标轴扩展
    plt.xlim(x_arr)


def mark_point(xy: tuple[float, float],
               size=50,
               pcolor="black",
               lcolor="black",
               style="--"):
    """绘制标记点并做辅助线

    Parameters
    ----------
    xy : tuple[float, float]
        标记点
    size : int, optional
        标记点大小, by default 50
    pcolor : str, optional
        标记点颜色, by default "black"
    lcolor : str, optional
        辅助线颜色, by default "black"
    style : str, optional
        辅助线样式, by default "--"
    """
    x_arr = plt.xlim()
    y_arr = plt.ylim()
    plt.scatter(xy[0], xy[1], s=size, c=pcolor)
    plt.plot([x_arr[0], xy[0]], [xy[1], xy[1]], c=lcolor, ls=style)
    plt.plot([xy[0], xy[0]], [y_arr[0], xy[1]], c=lcolor, ls=style)
    # 避免坐标轴扩展
    plt.xlim(x_arr)
    plt.ylim(y_arr)


if __name__ == "__main__":
    plt_style_init(Style.SETE)
    x = [1, 10]
    y = [[1, 9 - i] for i in range(5)]
    for i in range(5):
        plt.plot(x, y[i], label=f"line {i+1}")
    line_vertical(2)
    line_horizontal([3, 4, 7])
    mark_point([5, 5])
    post2d("y_i", ["x", r"y_{idx}"], {"idx": "1,2,3,4,5"})
    plt.show()
