# MgallManager

마이너 갤러리 관리 프로그램

-  자동 차단 기능
-  특정 유저 글 삭제 기능

실행 시 통신사 IP 차단을 1시간 주기로 자동 업데이트.

갤러리 관리자 권한이 있어야 이용 가능.

나머지 글 관리 기능 및 GUI 버전 추가 예정.

# 설치

pip -r requirements.txt


# 실행

아이디, 비밀번호 : 주석 지우고 auth.txt에 저장

밴 닉네임 리스트 : 주석 지우고 banned_users.txt에 저장

python main.py (갤러리 id) (모드)

block 모드 : 해당 갤러리에서 1시간 주기로 VPN 및 통신사 IP 차단 주기 갱신

delete 모드 : 해당 갤러리에서 1분 주기로 banned_users.txt에 있는 닉네임을 가진 글 삭제
