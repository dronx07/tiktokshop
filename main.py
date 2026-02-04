import streamlit as st
import requests
import json
from bs4 import BeautifulSoup

st.set_page_config(page_title="TikTok Shop (MVP)", layout="wide")
st.title("🧪 TikTok Shop (MVP)")

URL = st.text_input("Enter TikTok Shop URL")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.tiktok.com/",
    "Cookie": 'ttwid=1%7Cn5ek0jni80Qul-RR7wQmO3Mwcm0Ou1RKqS8OcnBra4w%7C1770208175%7Cf9fa6b23e9dfd9c02224ddf57b12880b625ef5c3ec74b45ce9b1b5e6189aec83; s_v_web_id=verify_ml808vy2_ZjCOm3xx_Y28B_4zv4_8DVk_fGVZW9pGI4sZ; dkms-type=3; dkms-token=MIIBDwQMlUzYlb0Vl4zkhg9jBIHsHGpGZnHQrwNGj1MoC84uAAyGJ7fbsgQi9BsqihDR854LzqoNN1aRdA/Ju6Es7nltIaxFZuMtqwLa3+NbtnlL/gdmiHfA2Pgc+pL1Tv1IEGTJlPeQmH6KQUkYpDvSdtYaTsf6sLDAsllm5eq1cisQl0/AiNW92unB40VKylNO1pKJRg+sXLzou6y2N36DG4fDDifOGLKB9mDw0sG18BNqSuncK92i2lNvGTnL913DWsCU/zKE9nKOxmY9d0nasfnZpmP5C+ZLQPaAHrHrxNaCzv60moWtD26+C/VQoNlu8qgu0/c00b/H9pyZHLwEEL4s+sueP62lJpdcUEvrhqs=; g_state={"i_l":0,"i_ll":1770208296159,"i_b":"bOgy1RMG/izQJG9MjAFiGchcRCwEZiTZV9ObO529BHg","i_e":{"enable_itp_optimization":0}}; msToken=0gxpqPQyPctVePFRF7i1eGk7aKKVrkgAZdIvu7BUb5UfhTUYPd0z9IDPNjp8A2qKOLGbvQSU7_FV_ZPB5Um8Q1qu0k4WKThYydUpNy0FKdxwVKNwM2K2z57PJucEAzakjg8_5bAE'
}

if st.button("Fetch & Parse"):
    if not URL:
        st.warning("Please enter a URL")
        st.stop()

    try:
        with st.spinner("Fetching page..."):
            response = requests.get(
                URL,
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()

        # 🔍 Detect blocking early
        if "__MODERN_ROUTER_DATA__" not in response.text:
            st.error("TikTok did NOT return expected data (likely blocked).")

            with st.expander("🔍 Raw response preview (first 2000 chars)"):
                st.text(response.text)

            st.stop()

        soup = BeautifulSoup(response.text, "lxml")
        script_tag = soup.find("script", id="__MODERN_ROUTER_DATA__")

        if not script_tag or not script_tag.string:
            st.error("Script tag found, but it is empty.")
            st.stop()

        data = json.loads(script_tag.string)

        st.success("Data extracted successfully 🎉")

        st.subheader("Parsed JSON")
        st.json(data)

    except requests.exceptions.RequestException as e:
        st.error("Network / request error")
        st.exception(e)

    except json.JSONDecodeError as e:
        st.error("JSON parsing failed")
        st.exception(e)

    except Exception as e:
        st.error("Unexpected error")
        st.exception(e)
