from flask import Flask, abort, request, json, Response
import pandas as pd
import re
import numpy as np
import sys
from datetime import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route('/api/analysis', methods = ['POST'])
def analyze():
	data = request.args
	file_name= data['file_name']
	messages = pd.DataFrame(columns=['date', 'time', 'sender', 'message','weekday','hour_of_day'])
	noramlizeRegex = re.compile(r'(^\d\d\/\d\d\/\d\d\d\d), (\d+:\d+\s\D+) - (.*?): (.*)')
	noramlizeRegex1 = re.compile(r'(^\d\d\/\d\d\/\d\d\d\d), (\d+:\d+\s\D+) - (.*)')
	with open('data/'+file_name) as fp:
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
	response = {}
	response['message_count'] = messages['sender'].value_counts().to_dict()
	response['the_talker'] = messages['sender'].value_counts().idxmax()
	response['the_silent_killer'] = messages['sender'].value_counts().idxmin()
	media=messages[(messages.message == '<Media omitted>')]
	response['media_count'] = media['sender'].value_counts().to_dict()
	response['media_share_freak'] = media['sender'].value_counts().idxmax()
	response['date_chart']=messages['date'].value_counts().to_dict()
	response['most_active_date']=messages['date'].value_counts().idxmax()
	response['active_day_of_week']=messages['weekday'].value_counts().idxmax()
	response['active_hour_of_day']=messages['hour_of_day'].value_counts().idxmax()
	return Response(json.dumps(response),  mimetype='application/json')

if __name__ == "__main__":
	app.run(debug=True)