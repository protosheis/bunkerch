from flask import render_template, redirect, url_for, request, abort
from flask_wtf import Form
from app import app, db
from .forms import PostForm
from .models import * 
from config import *
import json
import webassets
import re

#Set folder for images
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'

banglobal = db.session.query(Ban_global).all()

#Regex for >> backlinks
@app.template_filter('backlink')
def backlink(text):
    text = re.sub(r'&gt&gt&gt/([a-z]*)/([0-9]*)', r'<a href="/\1/\2">>>>/\1/\2</a>', text)
    text = re.sub(r'&gt&gt&gt/([a-z]*)/', r'<a href="/\1/">>>>\1</a>', text) 
    return re.sub(r'&gt&gt([0-9]*)', r'<a href="#\1">&gt&gt\1</a>', text) 

#Creates a filter for the html templates to check if something is a digi
@app.template_filter('isdig')
def isdig(text):
    return text[2].isdigit() 

app.jinja_env.filters['isdig'] = isdig
 
app.jinja_env.filters['backlink'] = backlink

#Escapes characters to sanitize DB input
@app.template_filter('escer')
def escer(text):
    offenders = FILTERS
    for k, v in offenders.items():
        text = re.sub(k, v, text, flags=re.IGNORECASE)
    chars = {
    '"': '&quot',
    '(': '&#40',
    ')': '&#41',
    ';': '&#59',
    '<': '&lt',
    '=': '&#61',
    '>': '&gt',
    '[': '&#91',
    '\': '#92',
    ']': '&#93',
    '{': '&#123',
    '}': '&#125',
    }
    for k, v in chars.items(): 
        text = text.replace(k, v)
    return text

app.jinja_env.filters['escer'] = escer

#Filter for code blocks
@app.template_filter('code')
def code(text):
    return re.sub(r'`(.*?)`', r'<span style="background-color: #DEDEDE;font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;">\1</span>', text)

#404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', SITE_NAME=SITE_NAME), 404

#403 page
@app.errorhandler(403)
def access_forbidden(e):
    return render_template('403.html', SITE_NAME=SITE_NAME), 403

#500 page
@app.errorhandler(500)
def oh_shit_issue(e):
    return render_template('500.html', SITE_NAME=SITE_NAME), 500 

#Creates the index page
import datetime
from .tripcode import tripcode
@app.route('/')
def index():
    boardlist = BOARDS.items()
    return render_template('home.html', boardlist=boardlist, SITE_NAME=SITE_NAME)

#Code for creating board index pages
@app.route('/<board>/', methods=['GET', 'POST'])
def board_b(board):
    if board not in BOARDS:
        abort(404)
    else:
        pass
    #Gets user's IP address
    if REVPROX == True:
        addre = request.headers.get("X-Forwarded-For").split(", ")[-1]
    else:
        addre = request.environ['REMOTE_ADDR']
    bind = False
    #Redirects banned users to ban page	
    for ban in banglobal:
        if ban.ip == addre:
            bind = True 
            return redirect("/banned", 302)
        else:
            pass
    for k, v in boardtabs.items():
        if k == board:
            posts = db.session.query(v)
        else:
            pass
    ports = posts.all()
    form = PostForm()
    if form.validate_on_submit():
        #Gets time user posted
        timey = datetime.datetime.utcnow()
        timey = timey.replace(microsecond=0)
        #If user inputs no name, change their name to "Anonymous"
        if form.name.data == "":
            form.name.data = 'Anonymous'
        else:
            #Sanitizes input
            chars = {
            '"': '&quot',
            '(': '&#40',
            ')': '&#41',
            ';': '&#59',
            '<': '&lt',
            '=': '&#61',
            '>': '&gt',
            '[': '&#91',
            '\': '#92',
            ']': '&#93',
            '{': '&#123',
            '}': '&#125',
            }
            for k, v in chars.items(): 
                form.name.data = form.name.data.replace(k, v)
            #Calls out users who attempt to impersonate mods or admins
            if '#' in form.name.data:
                if '##' in form.name.data:
                    form.name.data = form.name.data.replace('#', '&#35;')
                    form.name.data = form.name.data + ' <span style="color: red;">(This user is not a moderator or admin, even if they claim to be.)</span>'
                #Code for tripcodes
                else: 
                    form.name.data = form.name.data.split('#') 
                    form.name.data[1] = tripcode(form.name.data[1])
                    form.name.data = '</strong>!'.join(form.name.data)
                    form.name.data = form.name.data + '<strong>'
            else:
                pass
        #Code for actually sending the post through
        if form.subj.data != "" and not form.subj.data.startswith(" ") and bind == False:
            for k, v in boardtabs.items():
                if k == board:
                    post = v(body=form.post.data, timestamp=timey, trip=form.name.data, ip=addre, thread=None, bump=0, subject=form.subj.data)
                else:
                    pass
        elif bind == False:
            for k, v in boardtabs.items():
                if k == board:
                    post = v(body=form.post.data, timestamp=timey, trip=form.name.data, ip=addre, thread=None, bump=0, subject=None)
                else:
                    pass
        else:
            return redirect("/banned", 302)
        db.session.add(post)
        #Code for bumping threads
        for l in posts.all():
            tops = posts.filter_by(id=l.id).first() 
            if tops.bump is not None:
                tops.bump += 1
                if tops.bump >= 21:
                    db.session.delete(tops)
                else:
                    pass
            else:
                pass
        db.session.commit()
        return redirect('/%s/' % board)
    for k, v in BOARDS.items():
        if k != board:
            pass
        else:
           boardname = v
    return render_template('index.html', form=form, posts=ports, BOARD_LETTER=board, BOARD=boardname, list=list, SITE_NAME=SITE_NAME)

#Mostly the same as the code for board indexes
@app.route('/<board>/<int:thread_id>', methods=['GET', 'POST'])
def thread(board, thread_id):
    if board not in BOARDS:
        abort(404)
    else:
        pass
    if REVPROX == True:
        addre = request.headers.get("X-Forwarded-For").split(", ")[-1]
    else:
        addre = request.environ['REMOTE_ADDR']
    bind = False
    for ban in banglobal:
        if ban.ip == addre:
            bind = True
            return redirect("/banned", 302)
        else:
            pass
    for k, v in boardtabs.items():
        if k == board:
            posts = db.session.query(v)
        else:
            pass
    ports = posts.all()
    locke = False
    for i in posts.all():
        if i.id == thread_id and i.locked != None:
            locke = True
        else:
            pass
    limit = 0
    limitreached = False
    for post in posts.all():
        if post.id == thread_id and post.thread != None:
            abort(404)
        else:
            pass
    for m in posts.all():
        if m.thread == thread_id:
            limit += 1
        else:
            pass
    if limit >= 200:
        limitreached = True
    else:
        pots = posts.filter_by(id=thread_id).first()
        if posts.filter_by(id=thread_id).scalar() is not None:
            pass
        else:
            abort(404) 
        form = PostForm()
        if locke == False:
            if form.validate_on_submit():
                timey = datetime.datetime.utcnow()
                timey = timey.replace(microsecond=0)
                if form.name.data == "":
                    form.name.data = 'Anonymous'
                else:
                    chars = {
                    '"': '&quot',
                    '(': '&#40',
                    ')': '&#41',
                    ';': '&#59',
                    '<': '&lt',
                    '=': '&#61',
                    '>': '&gt',
                    '[': '&#91',
                    '\': '#92',
                    ']': '&#93',
                    '{': '&#123',
                    '}': '&#125',
                    }
                    for k, v in chars.items(): 
                        form.name.data = form.name.data.replace(k, v)
                    if '#' in form.name.data:
                        if '##' in form.name.data:
                            form.name.data = form.name.data.replace('#', '&#35;')
                            form.name.data = form.name.data + ' <span style="color: red;">(This user is not an admin, even if they claim to be.)</span>'
                        else: 
                            form.name.data = form.name.data.split('#') 
                            form.name.data[1] = tripcode(form.name.data[1])
                            form.name.data = '</strong>!'.join(form.name.data)
                            form.name.data = form.name.data + '<strong>'
                    else:
                        pass
                if form.opti.data == "age" or form.opti.data == "nokoage"  or form.opti.data == "noko" and bind == False:
                    for k, v in boardtabs.items():
                        if k == board:
                            post = v(body=form.post.data, timestamp=timey, trip=form.name.data, ip=addre, thread=thread_id, bump=None, sage=1)
                        else:
                            pass
                elif form.opti.data == "sage" or form.opti.data == "nokosage" and bind == False:
                    for k, v in boardtabs.items():
                        if k == board:
                            post = v(body=form.post.data, timestamp=timey, trip=form.name.data, ip=addre, thread=thread_id, bump=None, sage=0)
                        else:
                            pass
                elif bind == False:
                    for k, v in boardtabs.items():
                        if k == board:
                            post = v(body=form.post.data, timestamp=timey, trip=form.name.data, ip=addre, thread=thread_id, bump=None, sage=1)
                        else:
                            pass
                else:
                    return redirect("/banned", 302)
                db.session.add(post)
                #Code for letting users bump/age and sage posts
                if form.opti.data == "age" or form.opti.data == "nokoage":
                    if limitreached == False:
                        pots.bump = 0
                        for l in posts.all():
                            tops = posts.filter_by(id=l.id).first() 
                            if tops.bump is not None:
                                tops.bump += 1
                            else:
                                pass 
                    else:
                        pass
                db.session.commit()
                if ALWAYS_NOKO == True:
                    if form.opti.data == "nonokoage" or form.opti.data == "nonoko" or form.opti.data == "nonokosage":
                        return redirect('/%s/' % board)
                    else:
                        return redirect('/%s/%d' % (board, thread_id))
                else:
                    if form.opti.data == "nokoage" or form.opti.data == "noko" or form.opti.data == "nokosage":
                        return redirect('/%s/%d' % (board, thread_id))
                    else:
                        return redirect('/%s/' % board)
            for k, v in BOARDS.items():
                if k != board:
                    pass
                else:
                    boardname = v
            return render_template('thread.html', form=form, posts=ports, BOARD_LETTER=board, BOARD=boardname, thread_id=thread_id, list=list, int=int, SITE_NAME=SITE_NAME)
        else:
            return render_template('lockthread.html', posts=posts.ports, BOARD_LETTER=board, BOARD=boardname, thread_id=thread_id, list=list, int=int, SITE_NAME=SITE_NAME)

#Ban page, obviously 
#I think it was either unfinished or broken, either way I'll fix it soon enough
@app.route('/banned')
def banned():
    #Get user's IP address
    if REVPROX == True:
        addre = request.headers.get("X-Forwarded-For").split(", ")[-1]
    else:
        addre = request.environ['REMOTE_ADDR']
    return render_template('banned.html', addre=addre, banlist=banlist, banglobal=banglobal, SITE_NAME=SITE_NAME)
