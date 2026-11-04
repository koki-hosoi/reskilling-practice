"""予定表プログラム

使い方:
    py review-target.py 2026-10-02     指定した日の予定を時刻順に表示する
    py review-target.py                今日の予定を表示する

同じフォルダの schedule.json を読む。
"""

import json
import sys
from datetime import datetime, timezone


def load_schedule(path):
    """予定の一覧を JSON ファイルから読み込む。"""
    try:
        with open(path, encoding="utf-8") as f:
            events = json.load(f)
    except Exception:
        return []
    # 読みやすいように、開始時刻の順に並べ替えて保存し直しておく
    events.sort(key=lambda ev: ev["start"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    return events


def pick_by_date(events, date):
    """指定した日（"2026-10-02" の形）の予定だけを返す。"""
    return [ev for ev in events if ev["start"].startswith(date)]


def format_event(event):
    """予定1件を1行の文字列にする。"""
    start = event["start"][11:16]
    end = event["end"][11:16]
    location = event.get("location", "（場所なし）")
    return f"{start}-{end}  {event['title']}  @{location}"


def main():
    if len(sys.argv) >= 2:
        date = sys.argv[1]
    else:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    events = load_schedule("schedule.json")
    todays = pick_by_date(events, date)

    print(f"{date} の予定 {len(todays)} 件")
    for ev in todays:
        print(format_event(ev))


if __name__ == "__main__":
    main()
