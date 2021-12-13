import requests

def blocker(session: requests.Session):

    url = "https://gall.dcinside.com/ajax/managements_ajax/update_ipblock"
    session.headers["Referer"] = "https://gall.dcinside.com/mgallery/management/gallery?id=pessimism"
    a = session.cookies['ci_c']
    post_data = {
        "ci_t": session.cookies['ci_c'],
        "gallery_id": "pessimism",
        "_GALLTYPE_": "M",
        "proxy_time": 2880,
        "mobile_time": 60,
        "proxy_use": 1,
        "mobile_use": 1,
        "img_block_use": -1,
        "img_block_time": None
    }
    texts = ["proxy_time", "mobile_time"]
    if post_data["proxy_time"] > 0:
            post_data["proxy_use"] = 1
    else:
        post_data["proxy_use"] = 0

    if post_data["mobile_time"] > 0:
        post_data["mobile_use"] = 1
    else:
        post_data["mobile_use"] = 0

    response = session.post(url, data=post_data)
    if "fail" in response.text:
        print("Cannot manage gallery settings.")
    elif "success" in response.text:
        print(f"vpn 차단 : {post_data[texts[0]]//60}시간", end = ", ")
        print(f"통신사 IP 차단 : {post_data[texts[1]]}분")
