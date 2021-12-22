# MgallManager[GUI_ver]

마이너 갤러리 관리 프로그램

-  VPN 및 통신사 IP 차단(자동화)
-  특정 사용자 글 삭제(자동화)

기능 추가 예정.

- 차단 시간/글 삭제 주기 선택
- 미니 갤러리 관리

나머지 갤러리 관리 기능 추가 예정.

- 이미지, 동영상 첨부 관리
- 개념 추천/비추천 관리
- 코드 관리

# 필요 라이브러리 설치
```
pip -r requirements.txt
```

# 실행
```
python main.py
```
또는
```
pip install pyinstaller
pyinstaller -F -w --icon=orange.ico main.py --add-data="orange.ico;." --name Mgallmanager
```
또는 [실행 파일 다운로드](https://github.com/Gloriel621/MgallManager/releases/tag/v1.0.0)

![capture1](https://user-images.githubusercontent.com/65398406/147065794-668d8f6c-96f5-49fa-9d7f-7e44e970cdca.png)

1. 아이디와 비밀번호를 입력한 후 로그인합니다.

![capture2](https://user-images.githubusercontent.com/65398406/147081608-02d525ae-1885-483f-80d1-395962b82c50.png)

2. 접속하고자 하는 갤러리 id(영문)를 입력하여 해당 갤러리의 관리 페이지에 접근합니다.

![capture3](https://user-images.githubusercontent.com/65398406/147081646-fa29ec14-3dea-4676-a1cd-a355edf9f08c.png)

![capture4](https://user-images.githubusercontent.com/65398406/147081651-c215dd99-7ca3-4ad4-9a0e-517ee2ddbc24.png)

3. 현재 해당 갤러리의 VPN  및 통신사 IP 차단 상태를 확인합니다.
- '적용'을 눌러 고정된 시간만큼 한 번 차단을 활성화합니다.
- '자동 차단'을 눌러 일정 주기마다 차단을 갱신합니다.
- '차단 중지'를 눌러 차단을 비활성화할 수 있습니다.

![capture5](https://user-images.githubusercontent.com/65398406/147081654-fa559c75-f8b2-4c65-860d-37bd2cae2f85.png)

4. 사용자의 닉네임으로 필터링하여 해당하는 글을 삭제합니다.
- 삭제하고자 하는 닉네임 리스트를 ","로 나누어서 입력합니다.
- '글 삭제'를 눌러 해당 닉네임의 사용자 글을 한 번 삭제합니다.
- '자동 삭제'를 눌러 일정 주기마다 사용자의 글을 자동 삭제합니다.
- 기본 유동 닉네임 "ㅇㅇ"은 삭제하지 못하도록 고정했습니다.
