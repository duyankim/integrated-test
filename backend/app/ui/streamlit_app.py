import streamlit as st

def render_dashboard():
    st.title("배치 테스트 대시보드")
    
    # 배치 실행 상태
    col1, col2 = st.columns(2)
    with col1:
        st.metric("오늘의 테스트 성공률", "95%", "↑2%")
    
    # 배치별 실행 결과 테이블
    st.dataframe(get_batch_results())
    
    # 실행 버튼
    if st.button("테스트 실행"):
        run_batch_tests() 