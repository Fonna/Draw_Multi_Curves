import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy
from sympy.parsing.sympy_parser import parse_expr # 新增导入
# import math # math 模块不再直接需要，sympy 会处理

# 页面标题
st.title("函数曲线绘制器")
st.write("输入一个关于 'x' 的函数表达式来绘制 y = f(x) 的图像。")
st.write("例如: `x**2`, `sin(x)`, `1/x`, `x**3 - 2*x + 5`, `exp(-x**2)`")
st.write("支持常见的数学函数 (如 `sin`, `cos`, `tan`, `sqrt`, `log`, `exp`) 和常数 (`pi`, `E`)。") # 更新提示


# 输入函数表达式
func_str = st.text_input("输入函数 f(x):", "x**2")

# 输入 x 范围和点数
col1, col2, col3 = st.columns(3)
with col1:
    x_min = st.number_input("x 最小值:", value=-10.0)
with col2:
    x_max = st.number_input("x 最大值:", value=10.0)
with col3:
    num_points = st.number_input("点数:", value=400, min_value=10, step=10)

# 尝试生成和绘制图像
if func_str:
    try:
        # 生成 x 值
        x_vals = np.linspace(x_min, x_max, num_points)

        # --- 使用 SymPy 解析和计算 ---
        x_sym = sympy.symbols('x') # 定义符号 x
        # sympy_expr = sympy.parsing.mathematica.parse_mathematica(func_str) # 旧代码
        sympy_expr = parse_expr(func_str, local_dict={'x': x_sym}) # 修改后的解析方式

        # 将 sympy 表达式转换为 numpy 可用的函数
        # 'numpy' 模块使得 lambdify 可以使用 numpy 数组进行高效计算
        # 'math' 模块可以作为备选，但 numpy 通常更好
        # 'scipy' 也可以添加，如果需要 scipy 的特殊函数
        modules = ['numpy']
        func = sympy.lambdify(x_sym, sympy_expr, modules=modules)

        # st.write(f"解析后的 SymPy 表达式: `{sympy.latex(sympy_expr)}`") # 显示 LaTeX 格式的表达式
        # 使用 try-except 包装 latex 输出，以防表达式无法转换为 latex
        try:
            st.write(f"解析后的 SymPy 表达式: `{sympy.latex(sympy_expr)}`")
        except Exception as latex_err:
            st.write(f"无法生成表达式的 LaTeX 格式: {latex_err}")
            st.write(f"解析后的 SymPy 表达式 (原始): `{sympy_expr}`")


        # --- 执行计算 ---
        # 使用 np.errstate 来处理计算中可能出现的警告 (如除以零, log负数)
        with np.errstate(divide='ignore', invalid='ignore'):
            y_vals = func(x_vals)

        # 如果 y_vals 是一个标量（例如输入了常数表达式），则将其广播到 x_vals 的形状
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals)

        # 将结果中的 inf 替换为 nan，以便 matplotlib 正确绘制断点
        y_vals[np.isinf(y_vals)] = np.nan

        # --- 绘图 ---
        fig, ax = plt.subplots()

        # 检查 y_vals 是否与 x_vals 具有相同的形状
        if isinstance(y_vals, (np.ndarray, list)) and len(y_vals) == len(x_vals):
            ax.plot(x_vals, y_vals)
            ax.set_xlabel("x")
            ax.set_ylabel(f"y = {func_str}")
            ax.set_title(f"图像: y = {func_str}")
            ax.grid(True)

            # --- 改进的 Y 轴范围设置 ---
            y_finite = y_vals[np.isfinite(y_vals)] # 只考虑有限值
            if len(y_finite) > 1: # 需要至少两个点来确定范围
                y_min_plot = np.percentile(y_finite, 1) # 使用百分位数排除极端离群值
                y_max_plot = np.percentile(y_finite, 99)
                y_range = y_max_plot - y_min_plot
                # 添加一些边距，避免图像紧贴边界
                margin = y_range * 0.1 if y_range > 1e-6 else 0.5
                ax.set_ylim(y_min_plot - margin, y_max_plot + margin)
            elif len(y_finite) == 1: # 如果只有一个有限值
                 ax.set_ylim(y_finite[0] - 0.5, y_finite[0] + 0.5)
            else: # 如果没有有限值（例如 log(-1) over the whole range）
                 ax.set_ylim(-1, 1) # 设置一个默认范围

            st.pyplot(fig)
        # 这部分检查可能不再严格需要，因为 lambdify 通常会返回数组
        # 但保留以防万一 sympy 解析出常数
        elif np.isscalar(y_vals):
             st.warning(f"表达式 '{func_str}' 计算结果为一个常数 ({y_vals})。绘制为水平线。")
             fig, ax = plt.subplots()
             ax.plot(x_vals, np.full_like(x_vals, y_vals)) # 绘制水平线
             ax.set_xlabel("x")
             ax.set_ylabel(f"y = {func_str}")
             ax.set_title(f"图像: y = {func_str}")
             ax.grid(True)
             ax.set_ylim(y_vals - 0.5, y_vals + 0.5) # 设置 Y 轴范围
             st.pyplot(fig)
        else:
             st.error(f"计算得到的 y 值类型 ({type(y_vals)}) 不符合预期，无法绘图。")

    # 捕获 SymPy 解析错误 (可能需要调整捕获的异常类型)
    except (sympy.SympifyError, SyntaxError, TypeError, ValueError) as e: # 添加 ValueError
        st.error(f"解析函数表达式时出错: {e}")
        st.error("请检查你的表达式语法是否正确 (例如，使用 '*' 表示乘法)，并确保使用了支持的函数。")
    # 捕获其他可能的运行时错误
    except Exception as e:
        st.error(f"绘制图像时发生错误: {e}")
        st.error(f"请检查函数表达式和 x 范围。输入的表达式为: `{func_str}`")

else:
    st.info("请输入一个函数表达式。")

# 移除关于 eval 风险的警告，因为我们不再使用它
# st.caption("注意: 使用 `eval` 执行用户输入可能存在安全风险...")