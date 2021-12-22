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
pyinstaller -F -w --icon="icon/orange.ico" main.py -n Mgallmanager.exe
```
또는
```
실행파일을 다운로드하여 실행
```

![capture1](https://user-images.githubusercontent.com/65398406/147037070-ce24511d-381a-4a17-b41c-ecc03c20b4c1.png)

1. 아이디와 비밀번호를 입력한 후 로그인한다.
2. 접속하고자 하는 갤러리 id(영문)를 입력하여 관리자 권한을 확인한다.
3. VPN 또는 통신사 IP 차단
- 적용을 눌러 1회 차단한다.
- 자동 차단 활성화 시 중지하거나 프로그램을 끌 때까지 활성화된다.
4. 삭제하고자 하는 닉네임 리스트를 ","로 나누어서 입력한다.
- 글 삭제를 눌러 해당 닉네임을 가진 사용자의 글을 삭제한다.
-  자동 삭제를 눌러 선택한 주기대로 글을 삭제한다.
