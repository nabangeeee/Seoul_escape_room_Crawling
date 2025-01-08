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
    # 네이버 지도 열기
    driver.get("https://map.naver.com/v5/search/서울 방탈출")
    time.sleep(10)  # 페이지 로드 대기
    print("네이버 지도 열기 완료")

    # iframe 전환
    iframe = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#searchIframe"))
    )
    driver.switch_to.frame(iframe)
    print("iframe 전환 완료")
    time.sleep(5)

    # 장소 정보 크롤링
    results = []
    page = 1

    while True:  # 반복해서 페이지 크롤링
        print(f"현재 페이지: {page}")

        # 스크롤 대상 지정
        scrollable_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Ryr1F"))  # 검색 결과를 감싸는 div 선택자
        )

        # 스크롤 반복
        for _ in range(55):  # 원하는 만큼 스크롤 반복
            driver.execute_script("arguments[0].scrollTop += 500;", scrollable_div)
            time.sleep(1)  # 스크롤 후 대기

        # 장소 목록 가져오기
        places = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li._9v52G.UrAlx"))
        )
        print(f"검색 결과 개수: {len(places)}")

        for place in places:
            try:
                # 상호명 가져오기
                name_element = place.find_element(By.CSS_SELECTOR, "span.CMy2_")
                name = name_element.text.strip()
                print(f"상호명: {name}")

                # 주소 가져오기
                address_element = place.find_element(By.CSS_SELECTOR, "span.o_gX8.Zdfo0")
                address = address_element.text.strip()
                print(f"주소: {address}")

                # 결과 저장
                results.append({"상호명": name, "주소": address})
            except Exception as e:
                print(f"오류 발생: {e}")

        # "다음 페이지" 버튼 클릭
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="eUTV2" and span[text()="다음페이지"]]'))  # 버튼 선택자 수정
            )

            # 버튼 상태 확인
            aria_disabled = next_button.get_attribute("aria-disabled")
            print(f"다음 페이지 버튼 상태: {aria_disabled}")
            if aria_disabled == "true":  # 비활성화된 경우 크롤링 종료
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
df.to_csv("지도_서울_방탈출.csv", index=False, encoding="utf-8-sig")
print("CSV 파일로 저장 완료!")
