from flask import Blueprint, render_template
from datetime import datetime

LANGS = 'media/langs/'
SOCIALS = 'media/socials/'

views = Blueprint('views', __name__)

all_projects = [
    ('Apr 26, 2025', 'Managing tutoring with a simple frontend.', 'A project for Gimnazija Šentvid', 'https://github.com/lenartkladnik/tutorstvo-website'),
    ('Jan 5, 2025', 'Song recognition program for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Sngfetch'),
    ('May 10, 2025', 'Display system information with fully customizable ascii formatting.', 'Personal project', 'https://github.com/lenartkladnik/ascinfo', 'static/media/projects/ascinfo.png'),
    ('Aug 10, 2024', 'A python library for creating cli apps.', 'Personal project', 'https://github.com/lenartkladnik/CliUtils'),
    ('Apr 21, 2024', 'An interpreter for the Brainfuck esolang.', 'Personal project', 'https://github.com/lenartkladnik/Bf-Interpreter'),
    ('Apr 27, 2024', 'A simple 2 player chess game for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Chess'),
    ('May 25, 2024', 'A simple 1 player uno game for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Uno'),
    ('Nov 22, 2024', 'Display ascii weather info in the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Weather', 'static/media/projects/weather.png'),
    ('Jul 21, 2025', 'A music player and downloader in the terminal.', 'Personal project', 'https://github.com/lenartkladnik/musicplayer', 'static/media/projects/musicplayer.png')
]

all_projects = sorted(all_projects, key=lambda x: datetime.strptime(x[0], '%b %d, %Y'))[::-1]
new_projects = all_projects[0:2]

mail = 'lenart@kladnik.cc'

socials = [
    ('https://github.com/lenartkladnik', SOCIALS + 'github.svg'),
    ('https://youtube.com/@pyth0g', SOCIALS + 'youtube.svg'),
    ('mailto:' + mail, SOCIALS + 'mail.svg'),
    ('https://instagram.com/lenartkladnik', SOCIALS + 'instagram.svg')
]

display_socials = [x[0].replace('https://', '').replace('http://', '') for x in socials if 'mailto:' not in x[0]]

skills = [
    ('Python', LANGS + 'python.svg'),
    ('C++', LANGS + 'cpp.svg'),
    ('C', LANGS + 'c.svg'),
    ('JavaScript', LANGS + 'js.svg'),
    ('CSS', LANGS + 'css.svg'),
    ('Html', LANGS + 'html5.svg'),
    ('JSON', LANGS + 'json.svg'),
    ('Bash', LANGS + 'bash.svg')
]

@views.route('/')
def index():
    return render_template('index.html', socials=socials, projects=new_projects, skills=skills)

@views.route('/projects')
def projects():
    return render_template('projects.html', projects=all_projects)

@views.route('/contact')
def contact():
    return render_template('contact.html', socials=display_socials, mail=mail)
