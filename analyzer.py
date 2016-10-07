"""Processing Script."""
import hashlib
import os
import re
import sys
import numpy as np
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template, json, session
from datetime import datetime
from dateutil.parser import parse
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding("utf-8")

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = hashlib.sha1(os.urandom(128)).hexdigest()

bool_ = {"Date First": True, "Month First": False}


def allowed_file(filename):
    """Function to chcek the updated file format."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    """Function that does all the calculations."""
    if request.method == 'POST':
        attr = request.form['d_down']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = "ChatHistory" + datetime.now().strftime(
                "%Y%m%d%H%M%s") + ".txt"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            messages = pd.DataFrame(
                columns=['date', 'time', 'sender', 'message', 'weekday',
                         'hour_of_day'])

            with open('data/' + filename) as fp:
                for line in fp:
                    record = line.strip().split(" - ", 1)
                    if (len(record) == 1):
                        messages.loc[len(messages) + 1] = [np.nan, np.nan,
                                                           np.nan, line,
                                                           np.nan, np.nan]
                    else:
                        date_time = parse(record[0], dayfirst=bool_[attr])
                        info = record[1].split(":", 1)
                        if len(info) == 1:
                            messages.loc[len(messages) + 1] = [
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"), np.nan,
                                info[0], date_time.weekday(),
                                date_time.time().strftime("%H")
                            ]
                        else:
                            messages.loc[len(messages) + 1] = [
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"), info[0],
                                info[1], date_time.weekday(),
                                date_time.time().strftime("%H")
                            ]

            # Calculating stats from dataframe
            word_string = messages['message']
            ignore_words = [
                "omitted", "media", "a", "able", "about", "above", "abst",
                "accordance", "according", "accordingly", "across", "act",
                "actually", "added", "adj", "affected", "affecting", "affects",
                "after", "afterwards", "again", "against", "ah", "airport",
                "alarm", "alive", "all", "almost", "alone", "along", "already",
                "also", "although", "always", "am", "among", "amongst", "an",
                "and", "angry", "announce", "another", "answer", "any",
                "anybody", "anyhow", "anymore", "anyone", "anything", "anyway",
                "anyways", "anywhere", "apart", "app", "apparently",
                "application", "approximately", "are", "aren", "arent",
                "arise", "arm", "around", "as", "aside", "ask", "asking", "at",
                "auth", "available", "away", "awfully", "b", "back", "bad",
                "bag", "bake", "bar", "be", "became", "because", "become",
                "becomes", "becoming", "been", "beer", "before", "beforehand",
                "begin", "beginning", "beginnings", "begins", "behind",
                "being", "believe", "bell", "below", "bend", "beside",
                "besides", "between", "beyond", "bike", "bill", "biol", "bite",
                "boose", "boss", "both", "brief", "brief", "briefly", "bro",
                "buddy", "busy", "but", "button", "by", "c", "ca", "calculate",
                "calculated", "call", "called", "calm", "came", "can", "can't",
                "cannot", "cat", "cause", "causes", "certain", "certainly",
                "chat", "chair", "channel", "check", "close", "closing",
                "clue", "co", "code", "coffee", "com", "come", "comes",
                "company", "complete", "completed", "congrats", "contain",
                "containing", "contains", "could", "couldnt", "cow", "crash",
                "cross", "d", "da", "dai", "data", "database", "date",
                "daughter", "day", "db", "delete", "deleted", "desk", "did",
                "didn't", "diet", "different", "dinner", "do", "does",
                "doesn't", "dog", "doing", "don't", "done", "down",
                "downwards", "drive", "dude", "due", "during", "e-mail", "e",
                "each", "ear", "ear", "ears", "ease", "east", "easy", "ed",
                "edu", "effect", "eg", "eh", "eight", "eighty", "either",
                "else", "elsewhere", "email", "emp", "empty", "end", "ending",
                "enough", "error", "especially", "et-al", "et", "etc", "even",
                "evening", "ever", "every", "everybody", "everyone",
                "everything", "everywhere", "ex", "except", "exciting", "eye",
                "eyes", "f", "far", "fault", "female", "few", "ff", "fifth",
                "file", "first", "five", "fix", "flower", "fly", "followed",
                "following", "follows", "food", "for", "former", "formerly",
                "forth", "found", "four", "friday", "friend", "from", "fuck",
                "fun", "funny", "further", "furthermore", "g", "garbage",
                "gate", "gave", "gb", "get", "gets", "getting", "girl", "git",
                "give", "given", "gives", "giving", "glove", "go", "god",
                "goes", "gone", "good", "got", "gotten", "great", "gross",
                "guy", "h", "ha", "had", "hair", "hall", "happens", "hardly",
                "has", "hasn't", "hate", "have", "haven't", "having", "he",
                "hed", "hello", "hence", "her", "here", "hereafter", "hereby",
                "herein", "heres", "hereupon", "hers", "herself", "hes", "hi",
                "hid", "high", "him", "himself", "his", "hither", "ho", "holy",
                "home", "hope", "how", "howbeit", "however", "hundred",
                "husband", "i", "i'll", "i've", "id", "ie", "if", "im",
                "image", "immediate", "immediately", "importance", "important",
                "in", "inc", "increase", "increased", "indeed", "index",
                "information", "instead", "into", "invention", "inward",
                "iron", "is", "isn't", "it", "it'll", "itd", "its", "itself",
                "j", "junior", "just", "k", "keep", "keeps", "kept", "kg",
                "kid", "kids", "km", "know", "known", "knows", "l", "largely",
                "last", "lately", "later", "latter", "latterly", "laugh",
                "least", "leave", "leg", "legs", "less", "lest", "let", "lets",
                "life", "like", "liked", "likely", "line", "list", "little",
                "ll", "load", "lol", "look", "looking", "looks", "lost",
                "loud", "love", "low", "ltd", "lucky", "lunch", "m", "ma'am",
                "maam", "madam", "made", "mail", "mainmainly", "make", "makes",
                "male", "mam", "many", "marry", "matemay", "maybe", "mb", "me",
                "meal", "meals", "mean", "means", "meantime", "meanwhile",
                "men", "menu", "merely", "message", "mg", "might", "million",
                "mineral", "miss", "ml", "mobile", "monday", "monthly", "more",
                "moreover", "morning", "most", "mostly", "move", "movie", "mr",
                "mrs", "much", "mug", "must", "my", "myself", "n", "na",
                "name", "named", "namely", "nay", "nd", "near", "nearly",
                "necessarily", "necessary", "need", "needs", "neither",
                "never", "nevertheless", "new", "next", "nine", "ninety", "no",
                "nobody", "noise", "non", "none", "nonetheless", "noone",
                "nor", "normally", "north", "nos", "not", "noted", "nothing",
                "now", "nowhere", "np", "o", "obtain", "obtained", "obviously",
                "of", "off", "offer", "often", "oh", "ok", "okay", "old",
                "omitted", "on", "once", "one", "ones", "only", "onto", "open",
                "opening", "or", "ord", "other", "others", "otherwise",
                "ought", "our", "ours", "ourselves", "out", "outside", "over",
                "overall", "owing", "own", "p", "page", "pages", "part",
                "particular", "particularly", "past", "pattern", "pause",
                "pay", "pays", "pencil", "per", "perhaps", "phone", "photo",
                "picture", "ping", "placed", "play", "please", "pls", "plus",
                "pong", "poorly", "possible", "possibly", "potentially", "pp",
                "predominantly", "present", "previously", "primarily", "pro",
                "probably", "promise", "promptly", "proof", "proud", "provides",
                "pull", "push", "put", "q", "que", "quickly", "quiet", "quit",
                "quite", "qv", "r", "ran", "rather", "ratio", "rd", "re",
                "readily", "really", "recent", "recently", "ref", "refs",
                "regarding", "regardless", "regards", "related", "relatively",
                "reload", "reply", "research", "respectively", "restraunt",
                "resulted", "resulting", "results", "right", "rock", "rofl",
                "roll", "run", "s", "said", "same", "saturday", "saw", "say",
                "saying", "says", "script", "sec", "section", "see", "seeing",
                "seem", "seemed", "seeming", "seems", "seen", "self", "selves",
                "send", "senior", "sent", "sent", "seven", "several", "shall",
                "she", "she'll", "shed", "shes", "shit", "shock", "should",
                "shouldn't", "show", "showed", "shown", "showns", "shows",
                "shut", "significant", "significantly", "similar", "similarly",
                "since", "sir", "sirr", "six", "slightly", "slip", "smoke",
                "so", "some", "somebody", "somehow", "someone", "somethan",
                "something", "sometime", "sometimes", "somewhat", "somewhere",
                "son", "song", "soon", "sorry", "sort", "sound", "south",
                "specifically", "specified", "specify", "specifying", "sport",
                "sports", "still", "stop", "story", "strongly", "sub",
                "substantially", "successfully", "such", "sufficiently",
                "suggest", "sunday", "sup", "super", "superb", "sure", "take",
                "taken", "taking", "tall", "tea", "team", "tear", "tell",
                "temporary", "tends", "term", "test", "text", "th", "than",
                "thank", "thanks", "thanx", "that", "that'll", "that've",
                "thats", "the", "their", "theirs", "them", "themselves",
                "then", "thence", "there", "there'll", "there've",
                "thereafter", "thereby", "thered", "therefore", "therein",
                "thereof", "therere", "theres", "thereto", "thereupon",
                "these", "they", "they'll", "they've", "theyd", "theyre",
                "thing", "think", "this", "those", "thou", "though", "thoughh",
                "thousand", "throat", "throug", "through", "throughout",
                "thru", "thursday", "thus", "tight", "til", "till", "time",
                "tiny", "tip", "to", "today", "toe", "together", "too", "took",
                "tooth", "toward", "towards", "tower", "town", "translate",
                "tried", "tries", "truck", "truly", "trust", "try", "trying",
                "ts", "tuesday", "twice", "two", "u", "un", "under", "unfair",
                "unfortunately", "unless", "unlike", "unlikely", "until",
                "unto", "up", "update", "updated", "upon", "upper", "ups",
                "us", "use", "used", "useful", "usefully", "usefulness",
                "user", "uses", "using", "usually", "v", "value", "various",
                "ve", "very", "via", "visible", "viz", "vol", "vols", "volume",
                "vs", "w", "wake", "want", "wants", "was", "wash", "wasnt",
                "way", "we", "we'll", "we've", "web", "website", "wed",
                "wednesday", "weekend", "weekly", "welcome", "went", "were",
                "werent", "west", "what", "what'll", "whatever", "whats",
                "when", "whence", "whenever", "where", "whereafter", "whereas",
                "whereby", "wherein", "wheres", "whereupon", "wherever",
                "whether", "which", "while", "whim", "whither", "who",
                "who'll", "whod", "whoever", "whole", "whom", "whomever",
                "whos", "whose", "why", "widely", "wife", "will", "willing",
                "wish", "with", "within", "without", "women", "wont", "words",
                "work", "works", "world", "would", "wouldnt", "wrap", "wtf",
                "www", "x", "y", "ya", "yeah", "yep", "yes", "yesterday",
                "yet", "you", "you'll", "you've", "youd", "your", "youre",
                "yours", "yourself", "yourselves", "youth", "z", "zero",
                "things", "testing", "nice", "working", "messages", "issues",
                "issue", "refresh", "users", "upload", "download", "view",
                "free", "kool", "uh", "duh", "join", "joining", "original",
                "alright", "large", "entire", "start", "month", "sense", "fill"
            ]
            words = []
            for word in word_string:
                tt = word.lower()
                t = re.sub(r'[^\w]', ' ', tt)
                for word in t.split():
                    if "http" in word:
                        continue
                    if word not in ignore_words:
                        words.append(word)

            p = pd.Series(words)
            # get the counts per word
            freq = p.value_counts()
            # how many max words do we want to give back
            freq = freq.ix[0:25]

            response = {}
            response['word_cloud'] = freq.to_dict()
            response['message_count'] = messages['sender'].value_counts().head(
                10).to_dict()
            response['the_talker'] = messages['sender'].value_counts().idxmax()
            response['the_silent_killer'] = messages['sender'].value_counts(
            ).idxmin()
            media = messages[(messages.message == '<Media omitted>')]
            if len(media):
                response['media_count'] = media['sender'].value_counts(
                ).to_dict()
                response['media_share_freak'] = media['sender'].value_counts(
                ).idxmax()
            else:
                response['media_count'] = {}
                response['media_share_freak'] = ""
            response['date_chart'] = messages['date'].value_counts().to_dict()
            response['most_active_date'] = messages['date'].value_counts(
            ).idxmax()
            response['active_day_of_week'] = week_day(messages['weekday']
                                                      .value_counts().idxmax())
            response['active_hour_of_day'] = hour(messages['hour_of_day']
                                                  .value_counts().idxmax())
            response['avg_no_of_msgs_per_day'] = messages['date'].count(
            ) / messages['date'].nunique()
            session["data"] = json.dumps(response)
            return redirect(url_for('stats'))
    return render_template('index.html')


@app.route("/stats", methods=['GET'])
def stats():
    """Function to render stats page."""
    return render_template('stats.html', data=session["data"])


def week_day(x):
    """Function to return days of week."""
    return {0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'}[x]


def hour(x):
    """Function to return hour of day."""
    return {'0': '12 AM - 1 AM',
            '1': '01 AM - 2 AM',
            '02': '2 AM - 3 AM',
            '03': '3 AM - 4 AM',
            '04': '4 AM - 5 AM',
            '05': '5 AM - 6 AM',
            '06': '6 AM - 7 AM',
            '07': '7 AM - 8 AM',
            '08': '8 AM - 9 AM',
            '09': '9 AM - 10 AM',
            '10': '10 AM - 11 AM',
            '11': '11 AM - 12 PM',
            '12': '12 PM - 1 PM',
            '13': '1 PM - 2 PM',
            '14': '2 PM - 3 PM',
            '15': '3 PM - 4 PM',
            '16': '4 PM - 5 PM',
            '17': '5 PM - 6 PM',
            '18': '6 PM - 7 PM',
            '19': '7 PM - 8 PM',
            '20': '8 PM - 9 PM',
            '21': '9 PM - 10 PM',
            '22': '10 PM - 11 PM',
            '23': '11 PM - 12 AM'}[x]


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-p",
        "--port",
        dest="port",
        help="Port on which the app will run",
        default=5000)
    (options, args) = parser.parse_args()
    app.run(host='0.0.0.0', debug=True, port=int(options.port))
