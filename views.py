from flask import Blueprint, render_template, url_for
from datetime import datetime

views = Blueprint('views', __name__)

all_projects = [
    ('Apr 26, 2025', 'Managing tutoring with a simple frontend.', 'A project for Gimnazija Šentvid', 'https://github.com/lenartkladnik/tutorstvo-website'),
    ('Jan 5, 2025', 'Song recognition program for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Sngfetch'),
    ('May 10, 2025', 'Display system information with fully customizable ascii formatting.', 'Personal project', 'https://github.com/lenartkladnik/ascinfo'),
    ('Aug 10, 2024', 'A python library for creating cli apps.', 'Personal project', 'https://github.com/lenartkladnik/CliUtils'),
    ('Apr 21, 2024', 'An interpreter for the Brainfuck esolang.', 'Personal project', 'https://github.com/lenartkladnik/Bf-Interpreter'),
    ('Apr 27, 2024', 'A simple 2 player chess game for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Chess'),
    ('May 25, 2024', 'A simple 1 player uno game for the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Uno'),
    ('Nov 22, 2024', 'Display ascii weather info in the terminal.', 'Personal project', 'https://github.com/lenartkladnik/Weather')
]

all_projects = sorted(all_projects, key=lambda x: datetime.strptime(x[0], '%b %d, %Y'))[::-1]
new_projects = all_projects[0:2]

socials = [
    ('https://github.com/lenartkladnik', 'github.svg'),
    ('https://youtube.com/@pyth0g', 'youtube.svg'),
    ('mailto:lenart@kladnik.cc', 'mail.svg'),
    ('https://instagram.com/lenartkladnik', 'instagram.svg')
]

skills = [
    ('Python', 'python.svg'),
    ('C++', 'cpp.svg'),
    ('C', 'c.svg'),
    ('JavaScript', 'js.svg'),
    ('CSS', 'css.svg'),
    ('Html', 'html5.svg'),
    ('JSON', 'json.svg')
]

@views.route('/')
def index():
    return render_template('index.html', socials=socials, projects=new_projects, skills=skills)

@views.route('/projects')
def projects():
    return render_template('projects.html', projects=all_projects)

@views.route('/contact')
def contact():
    return render_template('contact.html', socials=socials)
