import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# 不再需要 math 库，因为 asteval 会处理常量如 pi, e
# import math
from asteval import Interpreter # 导入 asteval

# 设置字体为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']

st.title("函数曲线绘制器")

# --- 用户输入 ---
# 使用 st.columns 创建两列布局
col1, col2 = st.columns(2)

with col1:

    x_min = st.number_input("x 最小值:", value=-10.0)
    x_max = st.number_input("x 最大值:", value=10.0)

with col2:
    func_str = st.text_input("输入函数表达式 (例如 'sin(x)', 'x**2'):", "sin(x)")
    # 将点数滑块放在第二列，可以根据需要调整其他控件的位置
    num_points = st.slider("点数:", 50, 1000, 200, key="num_points_slider") # 添加 key 避免潜在冲突

# --- 函数计算 ---
x = np.linspace(x_min, x_max, num_points)
y = None
error_message = None

# 创建 asteval 解释器
aeval = Interpreter()

# 将需要用到的变量和函数添加到解释器的符号表中
# asteval 默认支持很多数学函数和常量 (sin, cos, pi, e 等)
# 我们只需要添加 numpy 数组 x 和 numpy 命名空间 np
aeval.symtable['x'] = x
aeval.symtable['np'] = np
# 也可以添加特定的 numpy 函数，如果不想暴露整个 np 命名空间
# aeval.symtable['sin'] = np.sin
# aeval.symtable['cos'] = np.cos
# ... etc ...

# 移除旧的 safe_dict 定义
# safe_dict = { ... }

try:
    # 使用 asteval 进行安全的表达式计算
    y = aeval(func_str)

    # 检查 asteval 是否有错误信息
    if aeval.error:
        # 将 asteval 的错误信息串联起来
        error_message = "; ".join([err.msg for err in aeval.error])
        st.error(f"函数表达式错误: {error_message}")
        y = None # 重置 y
        aeval.error = [] # 清除错误状态以便下次使用

    # 确保 y 是一个 numpy 数组，并且形状与 x 匹配 (asteval 通常会返回正确的类型)
    elif not isinstance(y, np.ndarray):
        # 如果结果是标量，则为每个 x 创建一个数组
        y = np.full_like(x, fill_value=y)
    elif y.shape != x.shape:
         st.error(f"计算结果的形状 {y.shape} 与 x 的形状 {x.shape} 不匹配。请检查函数表达式。")
         y = None # 重置 y 防止绘图错误

except Exception as e:
    # 捕获 asteval 本身可能抛出的其他异常 (虽然不太常见)
    error_message = f"计算时发生意外错误: {e}"
    st.error(error_message)
    y = None

# --- 绘图 ---
if y is not None and error_message is None:
    st.subheader("函数曲线") # 将子标题移到绘图部分之前

    # 使用 Matplotlib 绘图并进行美化
    plt.style.use('seaborn-v0_8-darkgrid') # 使用预设样式
    fig, ax = plt.subplots(figsize=(10, 6)) # 调整图形大小

    # 绘制美化后的曲线
    ax.plot(x, y,
            label=f'y = {func_str}',
            color='skyblue',      # 设置线条颜色
            linewidth=2.5,        # 设置线条宽度
            linestyle='-',        # 设置线条样式 ('-', '--', '-.', ':')
            marker='o',           # 添加数据点标记 ('o', 's', '^', etc.)
            markersize=4,         # 标记大小
            markeredgecolor='blue',# 标记边缘颜色
            markerfacecolor='lightblue' # 标记填充颜色
           )

    # 添加标题和标签
    ax.set_title(f'函数图像: y = {func_str}', fontsize=16)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)

    # 添加图例
    ax.legend(fontsize=10)

    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7) # 自定义网格线

    # 调整坐标轴范围（可选）
    # ax.set_xlim([x_min, x_max])
    # ax.set_ylim([min_y, max_y]) # 可以根据 y 的范围动态设置

    # 在 Streamlit 中显示图形
    st.pyplot(fig)

elif not error_message:
    st.info("请输入函数表达式并设置范围以查看曲线。")

# --- (可选) 显示原始数据 ---
# if y is not None and error_message is None:
#     st.subheader("数据点")
#     st.dataframe({'x': x, 'y': y})