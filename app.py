import streamlit as st
import requests
import json

# 페이지 설정 (아이콘을 배추로!)
st.set_page_config(page_title="Poggy의 수학 클리닉", page_icon="🥬")

# 1. 비밀번호(Webhook URL) 가져오기
WEBHOOK_URL = "https://bandalip.app.n8n.cloud/webhook/generate-math"

# 2. 화면 꾸미기
st.title("🥬 포기(Poggy)의 수학 클리닉")
st.markdown("""
> **"포기는 배추 셀 때나 하는 말이다!"** > 모르는 문제를 찍어 올리면, 기초부터 차근차근 알려줄게.
""")

uploaded_file = st.file_uploader("수학 문제 사진을 올려주세요", type=["jpg", "png", "jpeg"])

# 3. 사진이 올라오면 버튼 활성화
if uploaded_file is not None:
    st.image(uploaded_file, caption='질문할 문제', width=300)
    
    if st.button('포기 선생님, 도와주세요! 🆘', type="primary"):
        with st.spinner('포기가 배추잎 휘날리며 분석 중...🥬'):
            try:
                # n8n으로 사진 전송
                files = {'file': uploaded_file.getvalue()}
                response = requests.post(WEBHOOK_URL, files=files)
                
                # 결과 받기
                if response.status_code == 200:
                    # AI가 가끔 ```json ... ``` 이런거 붙여서 줄 때가 있어서 제거 작업
                    raw_text = response.text
                    clean_text = raw_text.replace("```json", "").replace("```", "").strip()
                    
                    try:
                        data = json.loads(clean_text)
                    except:
                        # JSON 변환 실패 시 그냥 텍스트로 보여주기 (비상용)
                        st.warning("포기가 말을 좀 꼬아서 했네... 일단 그대로 보여줄게!")
                        st.write(raw_text)
                        st.stop()

                    # --- 결과 화면 출력 ---
                    
                    # 1. 포기의 한마디
                    st.info(f"🥬 **Poggy:** {data.get('poggy_comment', '파이팅!')}")
                    
                    # 2. 정답 공개
                    st.subheader("✅ 정답")
                    st.write(data.get('solution', '정답을 못 찾았어...'))
                    
                    # 3. 친절한 풀이
                    st.subheader("📝 단계별 풀이")
                    st.markdown(data.get('step_by_step', '풀이 과정이 없습니다.'))
                    
                    # 4. 기초 파고들기 (Drill Down) - 핵심 기능!
                    st.markdown("---")
                    st.subheader("🔍 이 문제를 틀렸다면? (기초 다지기)")
                    
                    drill_downs = data.get('drill_down', [])
                    if drill_downs:
                        for item in drill_downs:
                            with st.expander(f"📌 {item['concept']}"):
                                st.markdown(item['explanation'])
                    else:
                        st.write("특별히 몰라도 되는 기초 개념은 없나 봐!")

                else:
                    st.error(f"서버가 아파... (에러코드: {response.status_code})")
            
            except Exception as e:
                st.error(f"연결 실패: {e}")
