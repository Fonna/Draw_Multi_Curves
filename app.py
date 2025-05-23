import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# 不再需要 math 库，因为 asteval 会处理常量如 pi, e
# import math
from asteval import Interpreter # 导入 asteval

# 设置字体为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']

def get_user_inputs():
    """参数输入，返回所有用户输入参数"""
    col1, col2, col3 = st.columns(3)
    with col1:
        x_min = st.number_input("x 最小值:", value=-10.0)
        x_max = st.number_input("x 最大值:", value=10.0)
    with col2:
        func_str1 = st.text_input("输入函数1表达式 (例如 'sin(x)', 'x**2'):", "sin(x)")
        func_str2 = st.text_input("输入函数2表达式 (例如 'cos(x)', 'x**3'):", "cos(x)")
        num_points = st.slider("点数:", 50, 1000, 200, key="num_points_slider")
    with col3:
        x_scale = st.slider("X轴缩放:", 0.1, 2.0, 1.0, 0.1)
        y_scale = st.slider("Y轴缩放:", 0.1, 2.0, 1.0, 0.1)
        show_func2 = st.checkbox("显示第二个函数", value=True)
    return x_min, x_max, func_str1, func_str2, num_points, x_scale, y_scale, show_func2


def compute_functions(x, func_str1, func_str2, show_func2):
    """表达式计算，返回y1, y2, error_message"""
    y1 = None
    y2 = None
    error_message = None
    aeval = Interpreter()
    aeval.symtable['x'] = x
    aeval.symtable['np'] = np
    try:
        y1 = aeval(func_str1)
        if aeval.error:
            error_message = "; ".join([err.msg for err in aeval.error])
            st.error(f"函数1表达式错误: {error_message}")
            y1 = None
            aeval.error = []
        elif not isinstance(y1, np.ndarray):
            y1 = np.full_like(x, fill_value=y1)
        elif y1.shape != x.shape:
            st.error(f"函数1计算结果的形状 {y1.shape} 与 x 的形状 {x.shape} 不匹配。")
            y1 = None
    except Exception as e:
        error_message = f"函数1计算时发生意外错误: {e}"
        st.error(error_message)
        y1 = None
    if show_func2:
        try:
            y2 = aeval(func_str2)
            if aeval.error:
                error_message = "; ".join([err.msg for err in aeval.error])
                st.error(f"函数2表达式错误: {error_message}")
                y2 = None
                aeval.error = []
            elif not isinstance(y2, np.ndarray):
                y2 = np.full_like(x, fill_value=y2)
            elif y2.shape != x.shape:
                st.error(f"函数2计算结果的形状 {y2.shape} 与 x 的形状 {x.shape} 不匹配。")
                y2 = None
        except Exception as e:
            error_message = f"函数2计算时发生意外错误: {e}"
            st.error(error_message)
            y2 = None
    return y1, y2, error_message


def plot_functions(x, y1, y2, func_str1, func_str2, x_min, x_max, x_scale, y_scale, show_func2):
    """绘图渲染"""
    st.subheader("函数曲线")
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    if y1 is not None:
        ax.plot(x, y1,
                label=f'y1 = {func_str1}',
                color='skyblue',
                linewidth=2.5,
                linestyle='-',
                marker='o',
                markersize=4,
                markeredgecolor='blue',
                markerfacecolor='lightblue')
    if y2 is not None and show_func2:
        ax.plot(x, y2,
                label=f'y2 = {func_str2}',
                color='lightcoral',
                linewidth=2.5,
                linestyle='-',
                marker='s',
                markersize=4,
                markeredgecolor='red',
                markerfacecolor='pink')
    ax.set_xlim([x_min * x_scale, x_max * x_scale])
    if y1 is not None or y2 is not None:
        y_min = min(np.min(y1) if y1 is not None else float('inf'),
                   np.min(y2) if y2 is not None else float('inf'))
        y_max = max(np.max(y1) if y1 is not None else float('-inf'),
                   np.max(y2) if y2 is not None else float('-inf'))
        y_range = y_max - y_min
        y_center = (y_max + y_min) / 2
        ax.set_ylim([y_center - y_range * y_scale / 2, y_center + y_range * y_scale / 2])
    ax.set_title('Curve Plotter', fontsize=16)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    # 默认绘制x轴和y轴
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    st.pyplot(fig)

# ================= 主流程 =================

st.set_page_config(page_title="函数曲线绘制器", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title("函数曲线绘制器")

x_min, x_max, func_str1, func_str2, num_points, x_scale, y_scale, show_func2 = get_user_inputs()
x = np.linspace(x_min, x_max, num_points)
y1, y2, error_message = compute_functions(x, func_str1, func_str2, show_func2)

if (y1 is not None or y2 is not None) and error_message is None:
    plot_functions(x, y1, y2, func_str1, func_str2, x_min, x_max, x_scale, y_scale, show_func2)
elif not error_message:
    st.info("请输入函数表达式并设置范围以查看曲线。")

# --- (可选) 显示原始数据 ---
# if y is not None and error_message is None:
#     st.subheader("数据点")
#     st.dataframe({'x': x, 'y': y})