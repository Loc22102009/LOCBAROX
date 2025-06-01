import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ai_model_lstm import AISoiCauLSTM
from pattern_detector import analyze_all_patterns

# Cấu hình trang & CSS hacker
st.set_page_config(page_title="TOOL NGUYỄN PHÚC LỘC", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #0f0f0f;
        color: #39ff14;
    }
    .stApp {
        background-color: black;
    }
    .stButton>button {
        background-color: #002200;
        color: #39ff14;
        border: 1px solid #39ff14;
    }
    .stButton>button:hover {
        background-color: #39ff14;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💻 TOOL NGUYỄN PHÚC LỘC – AI SOI CẦU TÀI XỈU LTMS 🧠")

def data_to_str(data):
    return ''.join(['T' if x == 1 else 'X' for x in data])

# Khởi tạo session_state để lưu lịch sử
if 'history' not in st.session_state:
    st.session_state.history = []

# Nút chọn Tài/Xỉu và xoá
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Tài (T)"):
        st.session_state.history.append(1)
with col2:
    if st.button("➕ Xỉu (X)"):
        st.session_state.history.append(0)
with col3:
    if st.button("🗑️ Xoá dữ liệu"):
        st.session_state.history = []

# Hiển thị chuỗi kết quả
st.subheader("📊 Chuỗi kết quả hiện tại:")
st.code(data_to_str(st.session_state.history), language="text")

# Vẽ biểu đồ bằng Plotly (nhúng vào placeholder để tái vẽ an toàn)
chart_placeholder = st.empty()
if len(st.session_state.history) > 0:
    x_vals = list(range(1, len(st.session_state.history) + 1))
    y_vals = st.session_state.history  # 0 hoặc 1
    labels = ['X' if d == 0 else 'T' for d in y_vals]

    fig = go.Figure(data=go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines+markers',
        marker=dict(color=['red' if d == 1 else 'blue' for d in y_vals], size=8),
        hovertext=labels,
        hoverinfo='x+text'
    ))
    fig.update_layout(
        title=dict(text="Biểu đồ kết quả Tài (1) / Xỉu (0)", font=dict(color='white')),
        xaxis=dict(title="Lần chơi", color='white'),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['X', 'T'],
            color='white'
        ),
        plot_bgcolor='black',
        paper_bgcolor='black'
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)
else:
    chart_placeholder.empty()

# Phân tích cầu và Dự đoán AI
if len(st.session_state.history) >= 10:
    if st.button("🚀 Phân tích và Dự đoán AI"):
        data = st.session_state.history

        # Phân tích cầu
        st.subheader("📈 Phân tích cầu:")
        patterns = analyze_all_patterns(data)
        for key, desc in patterns.items():
            st.markdown(f"- **{key}**: {desc}")

        # Dự đoán bằng LSTM
        st.subheader("🤖 Dự đoán AI (Cửa tiếp theo):")
        model = AISoiCauLSTM(window_size=10)
        try:
            model.train(data)
            pred = model.predict(data)
            ketqua = "TÀI (T)" if pred == 1 else "XỈU (X)"
            st.success(f"✅ AI dự đoán: **{ketqua}**")
        except Exception as e:
            st.error(f"Lỗi AI: {str(e)}")
else:
    st.warning("❗ Vui lòng nhập ít nhất 10 kết quả để phân tích và dự đoán.")

# Footer
st.markdown("---")
st.markdown("🔧 Tool by Nguyễn Phúc Lộc | Phân tích cầu nâng cao + LSTM")
