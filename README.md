# MgallManager [CLI_ver]

마이너 갤러리 관리 프로그램

-  VPN 및 통신사 IP 차단(자동화)
-  특정 사용자 글 삭제(자동화)

갤러리 관리자 권한이 있어야 이용 가능.


# 필요 라이브러리 설치
```
pip -r requirements.txt
```

# 실행

auth.txt 에 있는 주석을 지우고 자신의 아이디와 비밀번호를 입력하고 저장합니다.

주석 지우고 게시글을 삭제하고 싶은 사용자의 닉네임을 banned_users.txt에 저장합니다.

```
python main.py (갤러리 id) (모드)

예시) python main.py elsa block
```

# 모드

block 모드 : 해당 갤러리에서 즉시 1시간 동안 VPN 및 통신사 IP를 활성화하며, 59분 주기로 차단 주기를 갱신합니다.

delete 모드 : 해당 갤러리에서 1분 주기로 banned_users.txt에 저장된 닉네임을 가진 글을 삭제합니다.
