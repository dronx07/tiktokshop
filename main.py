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
