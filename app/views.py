from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm, oid
from forms import CreateForm, LoginForm, OpenIDForm, TagForm, SearchForm, GroupForm
from models import User, Tag, ROLE_USER, ROLE_ADMIN

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	if form.validate_on_submit():
		term = form.search.data
		return redirect(url_for('search',
			term=term))
	return render_template('index.html', 
		form=form)

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<term>', methods=['GET', 'POST'])
def search(term=None):
	form = SearchForm()
	if form.validate_on_submit():
		term = form.search.data
		return redirect(url_for('search',
			term=term))
	tag = Tag.find(term)
	if term and tag == None:
		flash("No results for that search")
		return redirect(url_for('index'))
	results = tag.search_related_tags()
	if len(results) == 0:
		flash("No results for that search")
		return redirect(url_for('index'))
	print(results)
	return render_template('search.html', 
		form=form,
		results=results)

@app.route('/user/<nickname>', methods=['GET', 'POST'])
def user(nickname, user=None):
	if user == None:
		user = User.user_for_nickname(nickname)
	if user == None:
		flash("That user doesn't exist")
		return redirect(url_for('index'))
	return render_template('user.html',
		user=user)

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/create', methods=['GET', 'POST'])
def create():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('profile'))
	createForm = CreateForm()
	if request.form:
		if request.form["submit"]:
			if request.form["submit"] == "Create":
				if createForm.validate_on_submit():
					remember_me = createForm.remember_me.data
					nickname = createForm.nickname.data
					email = createForm.email.data
					password = createForm.password.data
					confirm = createForm.confirmation.data
					user = User.user_for_email(email)
					if user is not None:
						flash("Account already exists for that email.")
						redirect("/login")
					elif password != confirm:
						flash("Passwords don't match.")
						redirect("/login")
					else:
						user = User(nickname=nickname, email=email, password=password, role=ROLE_USER)
						db.session.add(user)
						db.session.commit()
						login_user(user, remember=remember_me)
						return redirect(request.args.get('next') or url_for('index'))
	return render_template('create.html', 
		title='Create account', 
		create=createForm)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('profile'))
	loginForm = LoginForm()
	oidForm = OpenIDForm()
	if request.form:
		if request.form["submit"]:
			if request.form["submit"] == "Sign in":
				if loginForm.validate_on_submit():
					remember_me = loginForm.remember_me.data
					email = loginForm.email.data
					pw = loginForm.password.data
					user = User.user_for_email(email)
					if user is None or not user.check_password(pw):
						flash("No account matches that email/password.")
						return redirect("/login")
					else:
						login_user(user, remember=remember_me)	
						return redirect(request.args.get('next') or url_for('index'))
			elif request.form["submit"] == "Sign in using OpenID":
				if oidForm.validate_on_submit():
					session['remember_me'] = form.remember_me.data
					return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	
	return render_template('login.html', 
		title='Sign in', 
		login=loginForm, 
		openid=oidForm,
		providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		nickname = User.make_unique_nickname(nickname)
		user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = g.user
    group_form = GroupForm()
    tag_forms = []
    for group in user.groups:
        form = TagForm()
        form.group_name.data = group.name
        tag_forms.append(form)
    if request.form:
        if "add_group_input" in request.form:
            if group_form.validate_on_submit():
                return redirect(url_for('add_group', group_name=group_form.group_name.data))        
        else:
            i = 0
            for group in user.groups:
                if request.form["group_name"] == group.name:
                    form = tag_forms[i]            
                    if form.validate_on_submit():
                        return redirect(url_for('add_tag', tag_body=form.tag_body.data, group_name=group.name))
    return render_template('profile.html', 
        user=user, 
        group_form=group_form,
        tag_forms=tag_forms)
        
@app.route('/add_group/<group_name>')
@login_required
def add_group(group_name):
    if g.user.has_group(group_name):
        flash("You already have that group.")
    else:
        g.user.get_or_create_group(group_name)
    return redirect(url_for('profile'))
    
@app.route('/remove_group/<group_name>')
@login_required
def remove_group(group_name):
    if g.user.has_group(group_name):
        g.user.remove_group(group_name)
    return redirect(url_for('profile'))

@app.route('/add_tag/<tag_body>')
@app.route('/add_tag/<tag_body>/<group_name>')
@login_required
def add_tag(tag_body, group_name=None):
    tag = Tag.find_or_create(tag_body)
    group = g.user.get_or_create_group(group_name)
    user = g.user.add_tag(tag, group)
    if user:
    	db.session.add(user)
    	db.session.commit()
    return redirect(url_for('profile'))

@app.route('/remove_tag/<tag_body>')
@app.route('/remove_tag/<tag_body>/<group_name>')
@login_required
def remove_tag(tag_body, group_name=None):
    tag = db.session.query(Tag).filter(Tag.body == tag_body).first()
    group = g.user.get_group(group_name)
    if tag == None:
    	flash("You don't have that tag.")
    	return redirect(url_for('index'))
    user = g.user.remove_tag(tag, group)
    if user:
    	db.session.add(user)
    	db.session.commit()
    return redirect(url_for('profile'))

@app.route('/tag/<tag_body>')
def tag(tag_body):
	tag = db.session.query(Tag).filter(Tag.body==tag_body).first()
	if tag == None:
		flash("That tag doesn't exist.")
		return redirect(url_for('index'))
	return render_template('tag.html',
		tag=tag)


