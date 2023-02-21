## Setup

1. Install Python. Microsoft Store is a good option

2. Clone/Download this repo

3. Go to [the rammb-slider site](https://rammb-slider.cira.colostate.edu) and pick a view that you like. Copy the URL and set `SLIDER_URL` to it

4. Change any other configuration (e.g. Resolution and download directory)

5. Setup a cron job for every 10 mins.

   - Task Scheduler

   - Basic Task

   - on login

   - Start a program

     * program: `path\to\python3.exe` (MS Store: `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\python3.exe` where `<user>` is your username)

     * arguments: `app.py`

     * start in: `path\to\repo`

   - finish

   - edit Advanced Settings

   - Every 10 mins

## Details

I made this for myself using headless Firefox (Selenium) on Windows 11. No guarantees it will work on anything else or any promises on maintaining. Watch out for header/footer impacts on resolution. I thought it was cool so feel free to use for whatever. <3