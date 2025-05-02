from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import os

# Add the src directory to Python path to import scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_scraper():
    """Execute the web scraping job"""
    try:
        import scraper
        print("Scraping job completed successfully")
    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")

def main():
    scheduler = BlockingScheduler()
    
    # Schedule job_function to be called every day at 1 AM
    scheduler.add_job(
        run_scraper, 
        'cron', 
        hour=1,
        minute=0
    )
    
    print("Scheduler started. Scraper will run every day at 01:00 AM.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == '__main__':
    main()
