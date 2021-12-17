from flask import Flask
from flask import request
from flask import render_template
from covid_data_handler import covid_API_request, update_covid_data, schedule_covid_updates
from covid_news_handling import news_API_request, update_news, read_config
import sched
import time
import logging

logging.basicConfig(filename='logger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s - %(module)s - %(lineno)s ')


app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index_page():
    time = request.args.get('update')
    alarm_name = request.args.get('two')
    repeat = request.args.get('repeat')
    covid_data = request.args.get('covid-data')
    news = request.args.get('news')
    if time and (covid_data or news):
        if repeat:
            repeat=True
        else:
            repeat=False
        if covid_data:
            schedule_covid_updates(time,alarm_name,repeat)
        if news:
            pass
    else:
        logging.debug('Incomplete form was submitted')
    temp = read_config()
    (local_location, global_location, news_search_terms)=(temp["local_location"],temp["global_location"],temp["news_search_terms"])
    read_news = request.args.get('notif')
    articles = update_news(read_news,news_search_terms)
    (local_7day_infections,y,x,location) = update_covid_data(local_location,"ltla")
    (national_7day_infections,hospital_cases,deaths_total,nation_location) = update_covid_data(global_location,"nation")
    return render_template('index.html',
                           updates=[{"title":"update1", "content":"some stuff"},{"title":"2update","content":"jhdsfijsnfi"}],
                           title='I HATE THIS PROJECT',
                           location=location,
                           local_7day_infections=local_7day_infections,
                           nation_location=nation_location,
                           national_7day_infections= national_7day_infections,
                           hospital_cases= ("Daily Hospital Cases: ")+str(hospital_cases),
                           deaths_total= ("Total Deaths: ")+str(deaths_total),
                           news_articles=articles,
                           )




if __name__ == '__main__':
    app.run()
