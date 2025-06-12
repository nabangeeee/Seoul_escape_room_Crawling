# 🧭 Seoul Escape Room Crawler

**A Python web crawler that collects escape room business data from Naver Map**

This project aims to extract real-world escape room shop names and addresses in Seoul using Selenium automation on Naver Map. Although the final dataset was manually refined, this project demonstrates the initiative and technical process of automated data collection for building a recommendation system.

-----------------------------------------------

## 📌 Project Summary

- Crawled **Naver Map** search results for “서울 방탈출 (Seoul escape room)”
- Extracted:
  - 📍 Business Name (`상호명`)
  - 🏠 Address (`주소`)
- Automated multi-page scrolling and pagination using Selenium
- Exported final result to a CSV file for further processing

-----------------------------------------------

## 🧪 How to Run

1. Install dependencies:
   ```bash
   pip install selenium webdriver-manager pandas

-----------------------------------------------


## 📁 Repository Structure

   Seoul_escape_room_Crawling/
   
├── blog_naver_search.py           # Naver blog crawler for theme names

├── naver_map.py                   # Main crawler for Naver Map (store name, address)

├── 지도_서울_방탈출.csv              # Output CSV file with crawl results

├── 서울_방탈출_인생테마_블로그검출.csv  # blog crawl data

└── README.md                      # Project description

