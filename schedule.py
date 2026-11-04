import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


JST = timezone(timedelta(hours=9))


def load_schedule(path: Path):
    """schedule.json を読み込んで、予定のリストを返す。"""
    if not path.exists():
        raise FileNotFoundError(f"{path.name} が見つかりません。")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} の内容が配列ではありません。")

    return data


def filter_by_date(schedule, target_date: str):
    """指定した日付の予定だけを、開始時刻順に返す。"""
    target = datetime.strptime(target_date, "%Y-%m-%d").date()
    filtered = []#リストの変数(27行目)

    for item in schedule:
        start_text = item.get("start")
        if not start_text:
            continue
        try:
            start_dt = datetime.fromisoformat(start_text)
        except ValueError:
            continue
        if start_dt.date() == target:
            filtered.append(item)

    filtered.sort(key=lambda item: datetime.fromisoformat(item["start"]))
    return filtered


def format_event(item):
    """1件の予定を表示用の文字列に整える。"""
    start_dt = datetime.fromisoformat(item["start"])
    end_dt = datetime.fromisoformat(item["end"])

    start_text = start_dt.strftime("%H:%M")
    end_text = end_dt.strftime("%H:%M")
    title = item.get("title", "（タイトルなし）")
    location = item.get("location")

    if location:
        return f"{start_text}-{end_text}  {title}  @{location}"
    return f"{start_text}-{end_text}  {title}  ＠場所なし"


def main():
    if len(sys.argv) > 1:
        target_date = sys.argv[1]#文字列の変数(61行目)
    else:
        target_date = datetime.now(JST).strftime("%Y-%m-%d")

    try:
        schedule_path = Path(__file__).resolve().with_name("schedule.json")
        schedule = load_schedule(schedule_path)
        selected = filter_by_date(schedule, target_date)
    except FileNotFoundError as exc:
        print(f"{exc}\nスケジュールファイルがないため、表示できません。")
        return 1
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"schedule.json の内容が正しくありません: {exc}")
        return 1

    print(f"{target_date} の予定 {len(selected)} 件")#len(selected)←数の変数(76行目)

    for item in selected:
        print(format_event(item))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
