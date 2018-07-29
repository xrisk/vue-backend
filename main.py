from flask import Flask, jsonify, json
import sqlite3
import arrow


app = Flask(__name__)



@app.route('/api/events/<year>/<month>')
def get_calendar_data(year, month):
	conn = sqlite3.connect('calendar.db')
	c = conn.cursor()
	date = "{}-{}-__".format(year, str(month).zfill(2))
	c.execute("select date, title, desc, rowid from events where date LIKE ?", (date,))
	data = c.fetchall()
	resp = {}
	for row in data:
		event_date = row[0]
		event_title = row[1]
		event_descr = row[2]
		event_id = row[3]
		if not event_date in resp:
			resp[event_date] = []
		resp[event_date].append({
			"eventid": event_id,
			"title": event_title,
			"descr": event_descr
		})
	print(resp)
	return (json.dumps(resp), {
		"Access-Control-Allow-Origin": "*",
		"Access-Control-Allow-Methods": "GET"
	})

if __name__ == '__main__':
	app.run(debug=True)
	