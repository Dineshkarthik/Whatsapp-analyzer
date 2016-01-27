import os
from flask import Flask, request, redirect, url_for, render_template, json
from werkzeug import secure_filename
import pandas as pd
import re
import numpy as np
import sys
from datetime import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

data = None
@app.route("/", methods=['GET', 'POST'])
def index():
    global data
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            uniquename= "ChatHistory"+datetime.now().strftime("%Y%m%d%H%M%s")+".txt"
            filename = secure_filename(file.filename)
            # filename = secure_filename(file.'ChatHistory'+datetime.now().strftime("%Y%m%d%H%M%s")+'.txt')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniquename))
            messages = pd.DataFrame(columns=['date', 'time', 'sender', 'message','weekday','hour_of_day'])

            #Using regex to identify date,time,sender & message and loading to dataframe
            noramlizeRegex = re.compile(r'(^\d\d\/\d\d\/\d\d\d\d), (\d+:\d+\s\D+) - (.*?): (.*)')
            noramlizeRegex1 = re.compile(r'(^\d\d\/\d\d\/\d\d\d\d), (\d+:\d+\s\D+) - (.*)')
            with open('data/'+filename) as fp:
                for line in fp:
                    mo = noramlizeRegex.search(line)
                    if mo:
                        messages.loc[len(messages)+1] = [mo.group(1),datetime.strptime(mo.group(2), '%I:%M %p').time(),mo.group(3),mo.group(4),datetime.strptime(mo.group(1), '%d/%m/%Y').weekday(),datetime.strptime(mo.group(2), '%I:%M %p').time().strftime("%H")]
                    else:
                        no = noramlizeRegex1.search(line)
                        if no:
                            messages.loc[len(messages)+1] = [no.group(1),datetime.strptime(no.group(2), '%I:%M %p').time(),np.nan,no.group(3),datetime.strptime(no.group(1), '%d/%m/%Y').weekday(),datetime.strptime(no.group(2), '%I:%M %p').time().strftime("%H")]
                        else:
                            messages.loc[len(messages)+1] = [np.nan,np.nan,np.nan,line,np.nan,np.nan]

            #Calculating stats from dataframe
            response = {}
            response['message_count'] = messages['sender'].value_counts().to_dict()
            response['the_talker'] = messages['sender'].value_counts().idxmax()
            response['the_silent_killer'] = messages['sender'].value_counts().idxmin()
            media=messages[(messages.message == '<Media omitted>')]
            response['media_count'] = media['sender'].value_counts().to_dict()
            response['media_share_freak'] = media['sender'].value_counts().idxmax()
            response['date_chart'] = messages['date'].value_counts().to_dict()
            response['most_active_date'] = messages['date'].value_counts().idxmax()
            response['active_day_of_week'] = messages['weekday'].value_counts().idxmax()
            response['active_hour_of_day'] = messages['hour_of_day'].value_counts().idxmax()
            response['avg_no_of_msgs_per_day'] = messages['date'].count()/messages['date'].nunique()
            data = json.dumps(response)
            return redirect(url_for('stats'))
    return render_template('index.html')
   

@app.route("/stats", methods=['GET'])
def stats():
    return render_template('stats.html', data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)