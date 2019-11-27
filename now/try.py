import requests

resp = requests.get(
    "http://aqqmusic.tc.qq.com/amobile.music.tc.qq.com/"
    "M500001qvvgF38HVc4.mp3?guid=7332953645&vkey=BE0955C0"
    "18899A1CD5B9F2A47E8BE6524704F1197EECE1D28373D8392743"
    "C3F9C48519A23D835CFEB480A7452A4C33B45540E66B25DBF01E&uin=0&fromtag=8",
    headers={
        "Origin": "https://c.y.qq.com",
        "Referer": "https://c.y.qq.com",
    },
)

with open("surprise.mp3", "bw+") as f:
    f.write(resp.content)