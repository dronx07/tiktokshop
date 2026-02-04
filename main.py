import streamlit as st
import requests
import json
from bs4 import BeautifulSoup

st.set_page_config(page_title="TikTok Shop (MVP)", layout="wide")

st.title("🧪 TikTok Shop (MVP)")

URL = st.text_input("Enter URL")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/144.0.0.0 Safari/537.36"
    )
}

if st.button("Fetch & Parse"):
    if not URL:
        st.warning("Please enter a URL")
    else:
        try:
            with st.spinner("Fetching page..."):
                response = requests.get(URL, headers=headers, timeout=15)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            script_tag = soup.find("script", attrs={"id": "__MODERN_ROUTER_DATA__"})

            if not script_tag or not script_tag.string:
                st.error("Script tag __MODERN_ROUTER_DATA__ not found")
            else:
                data = json.loads(script_tag.string)

                st.success("Data extracted successfully 🎉")
                st.json(data)

        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
        except json.JSONDecodeError:
            st.error("Failed to decode JSON")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
