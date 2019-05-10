Deployment Step
===============
1. Add api settings to `config.py`
2. Change exchange name and other settings in `manifest.yml`
3. Change `crontab` for cron job setting
4. Change Python version in `runtime.txt` if needed
5. Deploy to cloud with command `cf push -b python_buildpack_offline -c './supercronic crontab 2>&1'`
Notice: quotes in command are different in Windows and others. 