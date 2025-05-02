from flask import Flask # Flask start 

app = Flask(__name__)

if not app.debug: # 디버그 모드가 아니면
    import logging  # 로깅을 하기위한 모듈
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler( # 2000바이트가 넘어가면 로테이팅 백업 진행. 최대 파일 10개
        'log/arambyeol_error.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING) # WARNING 수준의 레벨들을 로깅
    app.logger.addHandler(file_handler)

# 스케줄러 ---------------------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

def run_script():
    # 실행할 스크립트나 명령어를 여기에 추가
    subprocess.run(['python3', '/home/ubuntu/arambyeol/src/service/CrawlingService.py'])

# 백그라운드 스케줄러 생성
scheduler = BackgroundScheduler()
scheduler.add_job(run_script, 'cron', day_of_week='mon-fri', hour=1)

def start_scheduler():
    print("스케줄링 시작")
    scheduler.start()

# 애플리케이션이 종료될 때 스케줄러도 종료
def shutdown_scheduler(exception=None):
    scheduler.shutdown()

# 실행 ---------------------------------------------------------
if __name__ == '__main__':
    start_scheduler()
    app.run('0.0.0.0',port=80,debug=False, threaded=True)