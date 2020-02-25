"""Processing Script."""
import os
import re
import sys
import click
import hashlib
import numpy as np
import pandas as pd
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    json,
    session,
)

from datetime import datetime
from dateutil.parser import parse

UPLOAD_FOLDER = "data/"
ALLOWED_EXTENSIONS = set(["txt"])

app = Flask(__name__)
SESSION_TYPE = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = hashlib.sha1(os.urandom(128)).hexdigest()
app.config.from_object(__name__)

bool_ = {"Date First": True, "Month First": False}
text_file = open("ignore_words.txt", "r")
ignore_words = text_file.read().splitlines()
text_file.close()


def allowed_file(filename: str) -> bool:
    """Function to check the uploaded file format."""
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def is_date(string: str) -> bool:
    """Function to check if the string is date or not."""
    try:
        parse(string)
        return True
    except:
        return False


def get_dict(
    date: str,
    time: str,
    sender: str,
    message: str,
    weekday: str,
    hour_of_day: str,
) -> dict:
    """Return dictionary to build DF."""
    return dict(
        date=date,
        time=time,
        sender=sender,
        message=message,
        weekday=weekday,
        hour_of_day=hour_of_day,
    )


def week_day(x: int) -> str:
    """Function to return days of week."""
    return {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }[x]


def hour(x: str) -> str:
    """Function to return hour of day."""
    return {
        "00": "12 AM - 1 AM",
        "01": "01 AM - 2 AM",
        "02": "2 AM - 3 AM",
        "03": "3 AM - 4 AM",
        "04": "4 AM - 5 AM",
        "05": "5 AM - 6 AM",
        "06": "6 AM - 7 AM",
        "07": "7 AM - 8 AM",
        "08": "8 AM - 9 AM",
        "09": "9 AM - 10 AM",
        "10": "10 AM - 11 AM",
        "11": "11 AM - 12 PM",
        "12": "12 PM - 1 PM",
        "13": "1 PM - 2 PM",
        "14": "2 PM - 3 PM",
        "15": "3 PM - 4 PM",
        "16": "4 PM - 5 PM",
        "17": "5 PM - 6 PM",
        "18": "6 PM - 7 PM",
        "19": "7 PM - 8 PM",
        "20": "8 PM - 9 PM",
        "21": "9 PM - 10 PM",
        "22": "10 PM - 11 PM",
        "23": "11 PM - 12 AM",
    }[x]


def calculate_stats(file_name: str, attr: str) -> dict:
    """Calculates the values for visualisaiton."""
    _list = []

    with open(file_name) as fp:
        for line in fp:
            if not line.isspace():
                record = line.strip().split(" - ", 1)
                if len(record) == 1:
                    _list.append(
                        get_dict(np.nan, np.nan, np.nan, line, np.nan, np.nan)
                    )
                elif not (is_date(record[0])):
                    _list.append(
                        get_dict(np.nan, np.nan, np.nan, line, np.nan, np.nan)
                    )
                else:
                    date_time = parse(record[0], dayfirst=bool_[attr])
                    info = record[1].split(":", 1)
                    if len(info) == 1:
                        _list.append(
                            get_dict(
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"),
                                np.nan,
                                info[0],
                                date_time.weekday(),
                                date_time.time().strftime("%H"),
                            )
                        )
                    else:
                        _list.append(
                            get_dict(
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"),
                                info[0],
                                info[1],
                                date_time.weekday(),
                                date_time.time().strftime("%H"),
                            )
                        )
    messages = pd.DataFrame(_list)
    # Calculating stats from dataframe
    word_string = messages["message"]
    words = []
    for word in word_string:
        tt = word.lower()
        t = re.sub(r"[^\w]", " ", tt)
        for word in t.split():
            if "http" in word:
                continue
            if word not in ignore_words:
                words.append(word)

    p = pd.Series(words)
    # get the counts per word
    freq = p.value_counts()
    # how many max words do we want to give back
    freq = freq.iloc[0:25]

    stats = {}
    stats["word_cloud"] = freq.to_dict()
    stats["message_count"] = (
        messages["sender"].value_counts().head(10).to_dict()
    )
    stats["the_talker"] = messages["sender"].value_counts().idxmax()
    stats["the_silent_spectator"] = messages["sender"].value_counts().idxmin()
    media = messages[(messages.message == " <Media omitted>")]
    if len(media):
        stats["media_count"] = media["sender"].value_counts().to_dict()
        stats["media_share_freak"] = media["sender"].value_counts().idxmax()
    else:
        stats["media_count"] = {}
        stats["media_share_freak"] = ""
    stats["date_chart"] = messages["date"].value_counts().to_dict()
    stats["most_active_date"] = messages["date"].value_counts().idxmax()
    stats["active_day_of_week"] = week_day(
        messages["weekday"].value_counts().idxmax()
    )
    stats["active_hour_of_day"] = hour(
        messages["hour_of_day"].value_counts().idxmax()
    )
    stats["avg_no_of_msgs_per_day"] = round(
        messages["date"].count() / messages["date"].nunique(), 2
    )
    return stats


@app.route("/", methods=["GET", "POST"])
def index():
    """Function that does all the calculations."""
    if request.method == "POST":
        attr = request.form["d_down"]
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = (
                f"ChatHistory{datetime.now().strftime('%Y%m%d%H%M%s')}.txt"
            )
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            sid = hashlib.sha1(os.urandom(128)).hexdigest()
            session[sid] = json.dumps(
                calculate_stats("data/" + filename, attr)
            )
            response = redirect(url_for("stats"))
            response.set_cookie("session_id", sid)
            return response
    return render_template("index.html")


@app.route("/stats", methods=["GET"])
def stats():
    """Function to render stats page."""
    session_id = request.cookies.get("session_id")
    return render_template("stats.html", data=session.get(session_id))


def start(port):
    app.run(host="0.0.0.0", debug=True, port=int(port))
