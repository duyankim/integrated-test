import streamlit as st
import pytest
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def load_test_cases():
    test_cases = []
    test_path = Path("tests")
    
    # tests 디렉토리에서 test_*.py 파일들을 찾음
    for test_file in test_path.glob("test_*.py"):
        module_name = test_file.stem
        # 파일 내용을 읽어서 test로 시작하는 함수들을 찾음
        with open(test_file, 'r') as f:
            content = f.read()
            # 간단한 파싱: def test로 시작하는 라인 찾기
            for line in content.split('\n'):
                if line.strip().startswith('def test'):
                    test_name = line.split('def ')[1].split('(')[0]
                    test_cases.append({
                        'id': f"{module_name}::{test_name}",
                        'name': test_name,
                        'module': module_name,
                        'last_result': 'Not Run'
                    })
    
    return test_cases

def run_selected_tests(selected_tests):
    results = []
    for test in selected_tests:
        # pytest.main()으로 특정 테스트 실행
        result = pytest.main([test['id'], '-v'])
        results.append({
            'id': test['id'],
            'result': 'Pass' if result == 0 else 'Fail',
            'timestamp': datetime.now().isoformat()
        })
    return results

def main():
    st.title("테스트 실행 대시보드 📊")
    
    # 테스트 케이스 로드
    test_cases = load_test_cases()
    
    # 좌측: 테스트 케이스 그리드
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("테스트 케이스 목록")
        df = pd.DataFrame(test_cases)
        
        # AgGrid 스타일의 테이블로 표시
        selected_tests = st.data_editor(
            df,
            column_config={
                "last_result": st.column_config.SelectboxColumn(
                    "Result",
                    help="Test result",
                    options=["Pass", "Fail", "Not Run"],
                    required=True
                )
            },
            hide_index=True
        )
        
        # 선택된 테스트 실행 버튼
        if st.button("선택된 테스트 실행"):
            results = run_selected_tests(selected_tests)
            st.success(f"{len(results)}개 테스트 실행 완료!")
    
    # 우측: 테스트 결과 요약
    with col2:
        st.subheader("테스트 결과 요약")
        
        # 성공/실패 통계
        total = len(test_cases)
        passed = sum(1 for t in test_cases if t['last_result'] == 'Pass')
        failed = sum(1 for t in test_cases if t['last_result'] == 'Fail')
        
        # 원형 게이지로 성공률 표시
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (passed/total)*100 if total > 0 else 0,
            title = {'text': "성공률"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "darkgray"}
                ]
            }
        ))
        st.plotly_chart(fig)
        
        # 결과 뱃지 표시
        st.markdown(f"""
        ### 오늘의 테스트 현황
        - 🟢 성공: {passed}건
        - 🔴 실패: {failed}건
        - ⚪ 미실행: {total - passed - failed}건
        """)
        
        # 상세 리포트
        with st.expander("상세 테스트 리포트"):
            st.markdown("""
            ### 테스트 실행 내역
            | 시간 | 테스트명 | 결과 |
            |------|----------|------|
            """)
            # 여기에 상세 실행 내역 추가

if __name__ == "__main__":
    main()