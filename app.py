import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. 기본 설정 및 데이터 로드
# ---------------------------------------------------------
st.set_page_config(page_title="인사실 MBTI 카드 조회", layout="wide")

# 제목
st.title("📋 인사실 MBTI 카드 조회")

# 데이터 불러오기 (같은 폴더의 csv 파일)
# 캐싱을 사용하여 데이터가 바뀔 때만 다시 로드하도록 설정
@st.cache_data
def load_data():
    try:
        # 인코딩은 한글 깨짐 방지를 위해 'utf-8-sig' 또는 'cp949' 사용
        df = pd.read_csv('back_data.csv', encoding='utf-8-sig')
        # 데이터 전처리 (공백 제거 등)
        df['소속'] = df['소속'].astype(str).str.strip()
        df['MBTI'] = df['MBTI'].astype(str).str.upper().str.strip()
        return df
    except FileNotFoundError:
        st.error("데이터 파일(back_data.csv)을 찾을 수 없습니다.")
        return pd.DataFrame()

df = load_data()

# ---------------------------------------------------------
# 💡 추가된 부분: 16Personalities 검사 링크 버튼
# ---------------------------------------------------------
st.markdown("---") # 구분선
st.link_button("➡️ 내 MBTI 검사하러 가기!", "https://www.16personalities.com/ko")
st.markdown("---") # 구분선
# ---------------------------------------------------------


if not df.empty:
    # ---------------------------------------------------------
    # 2. 조회 모드 선택 (탭 구성)
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["🏢 팀별 조회 (A)", "🧩 MBTI 별 조회 (B)"])

    # --- [A] 팀별 조회 기능 ---
    with tab1:
        st.subheader("팀을 선택해주세요")
        
        # 팀 목록 추출 (중복 제거)
        teams = df['소속'].unique()
        
        # 팀 선택 버튼 생성 (가로로 나열하기 위해 columns 사용)
        # 팀이 많을 경우를 대비해 동적으로 컬럼 생성
        # 최대 5개의 컬럼으로 제한하고, 나머지는 다음 줄로 넘기기
        num_cols = min(len(teams), 5) 
        cols = st.columns(num_cols)
        
        selected_team = None
        
        # 각 팀별 버튼 생성
        for i, team in enumerate(teams):
            with cols[i % num_cols]: # num_cols 만큼 반복 후 다음 컬럼으로
                if st.button(f"{team}", key=f"btn_{team}", use_container_width=True):
                    selected_team = team
        
        st.divider() # 구분선
        
        if selected_team:
            st.markdown(f"### 📌 {selected_team} 구성원 명단")
            
            # 해당 팀 필터링
            team_df = df[df['소속'] == selected_team]
            
            # '이름', '소속', 'MBTI' 컬럼만 선택하여 보여주기
            # 인덱스는 숨기고 표 출력
            st.dataframe(
                team_df[['이름', '소속', 'MBTI']], 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.info("👆 위에서 조회하고 싶은 팀 버튼을 눌러주세요.")

    # --- [B] MBTI 별 조회 기능 ---
    with tab2:
        st.subheader("MBTI 유형별 구성원")
        
        # 16가지 MBTI 리스트 (순서대로 정렬)
        mbti_types = [
            "ISTJ", "ISFJ", "INFJ", "INTJ",
            "ISTP", "ISFP", "INFP", "INTP",
            "ESTP", "ESFP", "ENFP", "ENTP",
            "ESTJ", "ESFJ", "ENFJ", "ENTJ"
        ]
        
        # 4열 그리드로 배치
        rows = [mbti_types[i:i+4] for i in range(0, len(mbti_types), 4)]
        
        for row in rows:
            cols = st.columns(4)
            for idx, mbti in enumerate(row):
                with cols[idx]:
                    # MBTI 타이틀 스타일링
                    st.markdown(f"#### **{mbti}**")
                    st.markdown("---")
                    
                    # 해당 MBTI 필터링
                    target_people = df[df['MBTI'] == mbti]
                    
                    if not target_people.empty:
                        # 카드 형태로 출력 (이름 | 소속)
                        for _, person in target_people.iterrows():
                            st.write(f"**{person['이름']}** ({person['소속']})")
                    else:
                        st.caption("해당 없음")
                    
                    st.write("") # 간격 띄우기
                    st.write("") # 간격 띄우기

