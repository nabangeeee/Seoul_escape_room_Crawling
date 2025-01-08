import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ChromeDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 네이버 블로그 검색 결과 열기
    driver.get("https://search.naver.com/search.naver?ssc=tab.blog.all&query=%EC%84%9C%EC%9A%B8%20%EB%B0%A9%ED%83%88%EC%B6%9C%20%EC%9D%B8%EC%83%9D%ED%85%8C%EB%A7%88&sm=tab_opt&nso=so%3Add%2Cp%3Aall")
    time.sleep(5)  # 페이지 로드 대기
    print("네이버 블로그 검색 결과 열기 완료")

    # 제목 크롤링
    results = []
    page = 1

    while True:  # 반복해서 페이지 크롤링
        print(f"현재 페이지: {page}")

        # 스크롤 대상 확인 및 지정
        try:
            scrollable_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.api_subject_bx"))  # 스크롤 대상 확인
            )
            print("스크롤 대상 확인 완료")
        except Exception as e:
            print(f"스크롤 대상 찾기 실패: {e}")
            break

        # 스크롤 반복 (55번 제한)
        for _ in range(55):  # 원하는 만큼 스크롤 반복
            try:
                driver.execute_script("arguments[0].scrollTop += 500;", scrollable_div)
                time.sleep(1)  # 스크롤 후 대기
            except Exception as e:
                print(f"스크롤 중 오류 발생: {e}")
                break
        print("스크롤 완료")

        # 블로그 제목 가져오기
        titles = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.title_link"))
        )
        print(f"현재 페이지의 블로그 제목 수: {len(titles)}")

        for title in titles:
            try:
                title_text = title.text.strip()
                print(f"블로그 제목: {title_text}")

                # 결과 저장
                results.append({"블로그 제목": title_text})
            except Exception as e:
                print(f"오류 발생: {e}")

        # "다음 페이지" 버튼 클릭
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn_next"))
            )

            # 버튼 활성화 상태 확인
            if "disabled" in next_button.get_attribute("class"):  # 비활성화된 경우 크롤링 종료
                print("더 이상 페이지가 없습니다.")
                break

            # JavaScript로 버튼 클릭
            driver.execute_script("arguments[0].click();", next_button)
            print("다음 페이지로 이동")
            page += 1
            time.sleep(5)  # 페이지 전환 대기

        except Exception as e:
            print(f"페이지 이동 중 오류 발생: {e}")
            break

finally:
    driver.quit()

# DataFrame 생성 및 CSV 저장
df = pd.DataFrame(results)
df.to_csv("서울_방탈출_인생테마_블로그검색.csv", index=False, encoding="utf-8-sig")
print("CSV 파일로 저장 완료!")
