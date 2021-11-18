from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command='python dropParser.py')
job.minute.every(1)
cron.write()