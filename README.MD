# Streamlit 函数曲线绘制器

这是一个使用 Streamlit 构建的简单的 Web 应用程序，用于可视化和绘制数学函数曲线。

## 功能

*   输入数学函数表达式。
*   可视化函数在指定范围内的曲线。
*   （可能还有其他功能，您可以根据 `app.py` 的具体实现来补充）

## 安装

1.  **克隆仓库** (如果您是从 Git 仓库获取):
    ```bash
    git clone <your-repository-url>
    cd Streamlit_func_curve
    ```
2.  **创建虚拟环境** (推荐):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    # source venv/bin/activate
    ```
3.  **安装依赖**:
    假设您有一个 `requirements.txt` 文件（如果项目需要，请创建它）：
    ```bash
    pip install -r requirements.txt
    ```
    如果还没有 `requirements.txt`，至少需要安装 Streamlit：
    ```bash
    pip install streamlit
    ```
    （您可能还需要根据 <mcfile name="app.py" path="d:\Gitee\Streamlit_func_curve\app.py"></mcfile> 中的导入来安装其他库，例如 `numpy`, `matplotlib` 或 `plotly`）

## 使用方法

在项目根目录下运行以下命令启动 Streamlit 应用：

```bash
streamlit run app.py