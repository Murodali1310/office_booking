import argparse
from datetime import datetime
from booking.db import init_db, is_free, add_booking, get_current_booking
from booking.notifications import send_email, send_sms

DATE_FMT = "%Y-%m-%d %H:%M"


def check(args):
    start = datetime.strptime(args.start, DATE_FMT)
    end = datetime.strptime(args.end, DATE_FMT)
    if is_free(args.room, start, end):
        print(f"Кабинет {args.room} свободен с {args.start} до {args.end}")
    else:
        b = get_current_booking(args.room, start, end)
        print(f"Кабинет занят пользователем {b['user_name']} до {b['end_ts']}")


def book(args):
    start = datetime.strptime(args.start, DATE_FMT)
    end = datetime.strptime(args.end, DATE_FMT)
    if not is_free(args.room, start, end):
        b = get_current_booking(args.room, start, end)
        print(
            f"Нельзя забронировать: кабинет занят {b['user_name']} "
            f"до {b['end_ts']}"
        )
        return

    add_booking(
        args.room,
        args.user,
        args.email,
        args.phone,
        start,
        end,
    )
    print(f"Кабинет {args.room} успешно забронирован!")
    msg = f"Ваш кабинет: {args.room}\nВремя: {args.start} — {args.end}"

    try:
        send_email(args.email, "Бронь кабинета подтверждена", msg)
    except Exception as e:
        print(f"[WARNING] Не удалось отправить email: {e}")

    try:
        send_sms(args.phone, msg)
    except Exception as e:
        print(f"[WARNING] Не удалось отправить SMS: {e}")


def main():
    init_db()
    p = argparse.ArgumentParser(prog="office_booking")
    sub = p.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check")
    chk.add_argument("--room", type=int, required=True)
    chk.add_argument("--start", required=True, help=DATE_FMT)
    chk.add_argument("--end", required=True, help=DATE_FMT)
    chk.set_defaults(func=check)

    bkp = sub.add_parser("book")
    bkp.add_argument("--room", type=int, required=True)
    bkp.add_argument("--start", required=True, help=DATE_FMT)
    bkp.add_argument("--end", required=True, help=DATE_FMT)
    bkp.add_argument("--user", required=True)
    bkp.add_argument("--email", required=True)
    bkp.add_argument("--phone", required=True)
    bkp.set_defaults(func=book)

    args = p.parse_args()
    args.func(args)
