from matplotlib import pyplot as plt
from enum import Enum
from typing import Union
"""
Author: Eurka
Version: 0.2.0
ChangeLogs:
    2023-03-21 v0.2.0 新增绘图配色方案加载
    2022-10-24 v0.1.0 新增快速绘制 plot 图例和标识的功能
"""


class Style(Enum):
    SETE = 0
    NILOU = 1
    HUTAO = 2
    RAIDEN = 3
    N = 4


def _var_list2str(vars: list, hasBraket=True) -> str:
    """_var_list2str 辅助生成标准格式的变量文本，支持 Latex 数学表达式

    Args:
        vars (list): 变量列表
        hasBraket (bool, optional): 多变量是否加括号. Defaults to True.

    Returns:
        str: 标准格式的变量文本
    """
    if len(vars) == 1:
        return vars[0]
    if len(vars) > 1:
        return "(~" + ",~".join(vars) + "~)" if hasBraket else ",~".join(vars)


def _param_dict2str(params: dict) -> str:
    """_param_dict2str 辅助生成标准格式的函数参数文本，支持 Latex 数学表达式

    Args:
        params (dict): 函数参数

    Returns:
        str: 标准格式的函数参数文本
    """
    return ",~".join([f"{k}={v}" for (k, v) in params.items()])


def _build_plt_title(ans: str, vars: list[str], params: dict = None) -> str:
    """_build_plt_title 辅助生成标准格式的 pyplot 绘图的标题文本，支持Latex数学表达式
    
    e.g.:
        E vs x
        
        E vs x when k=0.1
        
        E vs (x, y) when k=0.1, g=0.98
    Args:
        ans (str): 函数值
        vars (list[str]): 变量
        params (dict, optional): 函数参数. Defaults to None.

    Returns:
        str: 绘图标题文本
    """
    var_str = _var_list2str(vars)
    if params is None:
        return f"${ans}$ vs ${var_str}$"
    return f"${ans}$ vs ${var_str}$ when ${_param_dict2str(params)}$"


def plt_style_init(style=Style.SETE):
    """plt_init 设置 matplotlib.pyplot 的全局绘图参数
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


def plt_post(ans: str, vars: list[str], params: dict = None, hasLabel=True):
    """plt_post 辅助生成标准格式的 pyplot 绘图标注，支持Latex数学表达式

    Args:
        ans (str): 函数值
        vars (list[str]): 变量
        params (dict, optional): 函数参数. Defaults to None.
        hasLabel (bool, optional): 是否绘制图例. Defaults to True.
    """
    plt.title(_build_plt_title(ans, vars, params))
    plt.xlabel(f"${_var_list2str(vars, False)}$")
    plt.ylabel(f"${ans}$")
    if hasLabel:
        plt.legend()


def plt_plot_line(x1y1: tuple[float, float],
                  x2y2: tuple[float, float],
                  color="black",
                  style="--"):
    """plt_plot_line 在 pyplot.plot 中快速绘制辅助线
    
    Tips:
        建议在 plot 之后调用

    Args:
        x1y1 (tuple[float, float]): 起始点1
        x2y2 (tuple[float, float]): 起始点2
        color (str, optional): 辅助线颜色. Defaults to "black".
        style (str, optional): 辅助线样式. Defaults to "--".
    """
    x_arr = [x1y1[0], x2y2[0]]
    y_arr = [x1y1[-1], x2y2[-1]]
    plt.plot(x_arr, y_arr, c=color, ls=style)


def plt_plot_line_vertical(x: Union[float, list[float]],
                           color="black",
                           style="--"):
    """plt_plot_line_vertical 在 pyplot.plot 中快速绘制垂直辅助线

    Tips:
        必须在 plot 之后调用
        
    Args:
        x (float): 辅助线位置
        color (str, optional): 辅助线颜色. Defaults to "black".
        style (str, optional): 辅助线样式. Defaults to "--".
    """
    y_arr = plt.ylim()
    if isinstance(x, list):
        for xi in x:
            plt.plot([xi] * 2, y_arr, c=color, ls=style)
    else:
        plt.plot([x] * 2, y_arr, c=color, ls=style)
    # 避免y轴方向坐标轴扩展
    plt.ylim(y_arr)


def plt_plot_line_horizontal(y: float, color="black", style="--"):
    """plt_plot_line_vertical 在 pyplot.plot 中快速绘制水平辅助线

    Tips:
        必须在 plot 之后调用
        
    Args:
        y (float): 辅助线位置
        color (str, optional): 辅助线颜色. Defaults to "black".
        style (str, optional): 辅助线样式. Defaults to "--".
    """
    x_arr = plt.xlim()
    if isinstance(y, list):
        for yi in y:
            plt.plot(x_arr, [yi] * 2, c=color, ls=style)
    else:
        plt.plot(x_arr, [y] * 2, c=color, ls=style)
    # 避免x轴方向坐标轴扩展
    plt.xlim(x_arr)


if __name__ == "__main__":
    plt_style_init(Style.SETE)
    x = [1, 2, 3, 4, 5]
    y1 = [3, 2, 3, 1, 5]
    y2 = [4, 1, 2, 5, 3]
    y3 = [2, 5, 1, 4, 3]
    y4 = [1, 2, 1, 5, 3]
    y5 = [2, 2, 3, 4, 5]
    for i in range(5):
        plt.plot(x, eval(f"y{i+1}"), label=f"line {i+1}")
    plt_plot_line_vertical(2)
    plt_plot_line_horizontal([3, 5, 7])
    plt.legend()
    plt.show()