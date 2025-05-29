pip install streamlit pandas plotly
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="2025 VOC 대시보드", layout="wide")

# 데이터 로딩
@st.cache_data
def load_data():
    file_path = "voc_data.xlsx"  # 엑셀 파일명을 여기에 맞게 수정
    daily_df = pd.read_excel(file_path, sheet_name="일일업무처리결과")
    stats_df = pd.read_excel(file_path, sheet_name="통계")
    daily_df['접수일자'] = pd.to_datetime(daily_df['접수일자'])
    daily_df['처리일자'] = pd.to_datetime(daily_df['처리일자'], errors='coerce')
    return daily_df, stats_df

daily_df, stats_df = load_data()

# 제목
st.title("🏢 교육문화팀 2025년 VOC 및 시설개선 대시보드")

# KPI 카드
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 VOC 건수", f"{len(daily_df)} 건")
with col2:
    avg_days = daily_df['처리기간'].mean()
    st.metric("평균 처리 기간", f"{avg_days:.1f} 일")
with col3:
    success_rate = (daily_df['처리결과'] == "의견수용").mean() * 100
    st.metric("의견수용률", f"{success_rate:.1f}%")

st.divider()

# 📊 월별 시설개선 추이
st.subheader("📈 월별 시설개선 건수")
monthly_stats = stats_df.groupby('월')['시설개선(건)'].sum().reset_index()
fig1 = px.bar(monthly_stats, x='월', y='시설개선(건)', text='시설개선(건)', title='월별 시설개선 건수')
st.plotly_chart(fig1, use_container_width=True)

# 📍 장소별 VOC 빈도
st.subheader("📍 VOC 발생 장소 Top 10")
top_places = daily_df['발생장소'].value_counts().head(10).reset_index()
top_places.columns = ['장소', '건수']
fig2 = px.bar(top_places, x='건수', y='장소', orientation='h', text='건수', title='장소별 VOC 건수 Top 10')
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# 📋 VOC 상세 목록 (필터 포함)
st.subheader("📋 VOC 상세 리스트")

# 필터
col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox("월 선택", options=['전체'] + sorted(daily_df['접수일자'].dt.month.unique().tolist()))
with col2:
    selected_place = st.selectbox("장소 선택", options=['전체'] + sorted(daily_df['발생장소'].dropna().unique().tolist()))

# 필터 적용
filtered_df = daily_df.copy()
if selected_month != '전체':
    filtered_df = filtered_df[filtered_df['접수일자'].dt.month == selected_month]
if selected_place != '전체':
    filtered_df = filtered_df[filtered_df['발생장소'] == selected_place]

# 테이블 출력
st.dataframe(
    filtered_df[['접수일자', 'VOC 및 시설개선', '발생장소', '처리내용', '처리일자', '처리결과']].sort_values(by='접수일자', ascending=False),
    use_container_width=True,
    height=400
)
