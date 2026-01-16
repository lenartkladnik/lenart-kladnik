from flask import Blueprint, render_template, request
from datetime import datetime
from dtf import DynamicTextFormat
from resources import background_color, bold, color, end_color, box, italic, side_to_side, visual_center

LANGS = 'media/langs/'
SOCIALS = 'media/socials/'

views = Blueprint('views', __name__)

all_projects = [
    (
        'Apr 26, 2025',
        'Managing tutoring with a simple frontend.',
        'A project for Gimnazija Šentvid',
        'https://github.com/lenartkladnik/tutorstvo-website',
        '',
        'Tutoring website',
        'Tutoring managment frontend'
    ),
    (
        'Jan 5, 2025',
        'Song recognition program for the terminal.',
        'Personal project',
        'https://github.com/lenartkladnik/Sngfetch',
        '',
        'Sngfetch',
        'Recognize a song in the terminal'
    ),
    (
        'May 10, 2025',
        'Display system information with fully customizable ascii formatting.',
        'Personal project',
        'https://github.com/lenartkladnik/ascinfo',
        'static/media/projects/ascinfo.png',
        'ascinfo',
        'Display system info with fancy ascii formatting'
    ),
    (
        'Aug 10, 2024',
        'A python library for creating TUI apps.',
        'Personal project',
        'https://github.com/lenartkladnik/CliUtils',
        '',
        'CliUtils',
        'TUI helper lib'
    ),
    (
        'Apr 21, 2024',
        'An interpreter for the Brainfuck esolang.',
        'Personal project',
        'https://github.com/lenartkladnik/Bf-Interpreter',
        '',
        'Bf-Interpreter',
        'Brainfuck interpreter'
    ),
    (
        'Apr 27, 2024',
        'A simple 2 player chess game for the terminal.',
        'Personal project',
        'https://github.com/lenartkladnik/Chess',
        '',
        'Chess',
        'Chess in the terminal'
    ),
    (
        'May 25, 2024',
        'A simple 1 player uno game for the terminal.',
        'Personal project',
        'https://github.com/lenartkladnik/Uno',
        '',
        'Uno',
        'Uno in the terminal'
    ),
    (
        'Nov 22, 2024',
        'Display ascii weather info in the terminal.',
        'Personal project',
        'https://github.com/lenartkladnik/Weather',
        'static/media/projects/weather.png',
        'CliWeather',
        'Weather in the terminal'
    ),
    (
        'Jul 21, 2025',
        'A music player and downloader in the terminal.',
        'Personal project',
        'https://github.com/lenartkladnik/musicplayer',
        'static/media/projects/musicplayer.png',
        'MusicPlayer',
        'Play and download music in the terminal'
    )
]

all_projects = sorted(all_projects, key=lambda x: datetime.strptime(x[0], '%b %d, %Y'))[::-1]
new_projects = all_projects[0:2]

mail = 'lenart@kladnik.cc'

socials = [
    ('https://github.com/lenartkladnik', SOCIALS + 'github.svg', 'GitHub'),
    ('https://youtube.com/@pyth0g', SOCIALS + 'youtube.svg', 'Youtube'),
    ('mailto:' + mail, SOCIALS + 'mail.svg', 'Mail'),
    ('https://instagram.com/lenartkladnik', SOCIALS + 'instagram.svg', 'Instagram')
]

display_socials = [x[0].replace('https://', '').replace('http://', '') for x in socials if 'mailto:' not in x[0]]

skills = [
    (
        'Python',
        LANGS + 'python.svg',
        f'  {color("blue")}ϾΞΞΞ╗{end_color()}\n {color("blue")}╔ΞΞΞΞ╝{color("yellow")}╗{end_color()}\n {color("blue")}╚{color("yellow")}╔ΞΞΞΞ╝{end_color()}\n  {color("yellow")}╚ΞΞΞϿ{end_color()}'
    ),
    (
        'C++',
        LANGS + 'cpp.svg',
        f'{color("light-blue")}🭈🭆🭂█🭍🭑🬽{end_color()}\n{color("light-blue")}█{color("white")}{background_color("light-blue")} 𜵎𜷋𜷋{background_color("light-blue")}𜹠{color("mid-blue")}🭅{end_color()}\n{color("light-blue")}{background_color("dark-blue")}🭝{color("light-blue")}🭚{end_color()}{color("white")}{background_color("dark-blue")}𜴇🬁🬁{color("mid-blue")} 🭖{end_color()}\n{color("dark-blue")}🭣🭧🭓█🭞🭜🭘{end_color()}'
    ),
    (
        'C',
        LANGS + 'c.svg',
        f'{color("light-blue")}🭈🭆🭂█🭍🭑🬽{end_color()}\n{color("light-blue")}█{color("white")}{background_color("light-blue")}  𜵎 {background_color("light-blue")} {color("mid-blue")}🭅{end_color()}\n{color("light-blue")}{background_color("dark-blue")}🭝{color("light-blue")}🭚{end_color()}{color("white")}{background_color("dark-blue")} 𜴇 {color("mid-blue")} 🭖{end_color()}\n{color("dark-blue")}🭣🭧🭓█🭞🭜🭘{end_color()}'

    ),
    (
        'JavaScript',
        LANGS + 'js.svg',
        f'{background_color("yellow")}        {end_color()}\n{background_color("yellow")}        {end_color()}\n{background_color("yellow")}{color("black")}    🬓𜵎𜴀 {end_color()}\n{background_color("yellow")}{color("black")}   𜴫𜴍𜴪𜴍 {end_color()}'),
    (
        'CSS',
        LANGS + 'css.svg',
        f'{background_color("darker-purple")}        {end_color()}\n{background_color("darker-purple")}        {end_color()}\n{background_color("darker-purple")}{color("white")}  𜵎𜴀𜵎𜴀𜵎𜴀{end_color()}\n{background_color("darker-purple")}{color("white")}  𜴬𜴉𜴪𜴍𜴪𜴍{end_color()}'
    ),
    (
        'Html',
        LANGS + 'html5.svg',
        f'{color("orange")} 🬦🬹🬹🬹🬹🬓\n{color("orange")}▐{color("white")}{background_color("orange")} 𜷇𜶷 {end_color()}{color("orange")}▌\n{color("orange")} 🭦{color("white")}{background_color("orange")} 𜴜𜴒 {end_color()}{color("orange")}🭛{end_color()}\n{color("orange")}🭣🭧🭜🭘{end_color()}'
    ),
    (
        'JSON',
        LANGS + 'json.svg',
        f'{color("mid-gray")} 🬵𜴈🬂🬂🬂𜴇🬱{end_color()}\n{color("mid-gray")} █     █{end_color()}\n{color("mid-gray")} █     █{end_color()}\n{color("mid-gray")} 𜴅𜴣𜴧𜴧𜴧𜴔𜴂{end_color()}'
    ),
    (
        'Bash',
        LANGS + 'bash.svg',
        f'{color("mid-gray")}🭇🬭🬭🬭🬭🬼{end_color()}\n{color("mid-gray")}▐{color("white")}(🭽  {color("mid-gray")}▌{end_color()}\n{color("mid-gray")}▐{color("white")}🭿)__{color("mid-gray")}▌{end_color()}\n{color("mid-gray")}🭢🬂🬂🬂🬂🭗{end_color()}'
    )
]

text_response = ["curl", "python", "binget", "java", "perl", "php", "pycurl", "go-http"]

@views.route('/')
def index():
    if any([x in request.headers["User-Agent"].lower() for x in text_response]):
        return DynamicTextFormat.render_text("index.dtf", color=color,
                                             end_color=end_color, skills=skills,
                                             background_color=background_color,
                                             bold=bold, socials=socials,
                                             box=box, italic=italic,
                                             all_projects=all_projects,
                                             new_projects=new_projects,
                                             side_to_side=side_to_side,
                                             visual_center=visual_center,
                                            )

    return render_template('index.html', socials=socials, projects=new_projects, skills=skills)

@views.route('/projects')
def projects():
    if any([x in request.headers["User-Agent"].lower() for x in text_response]):
        return "Hello world!"

    return render_template('projects.html', projects=all_projects)

@views.route('/contact')
def contact():
    if any([x in request.headers["User-Agent"].lower() for x in text_response]):
        return "Hello world!"

    return render_template('contact.html', socials=display_socials, mail=mail)
