from flask import Blueprint, render_template, session
from app.models import Post
from app.utils.auth import login_required
from app.db import get_db
# using the url_prefix argument, we prefix every route in the blueprint with /dashboard. The routes thus become /dashboard and /dashboard/edit/<id> when registered with the app
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dash():
    db = get_db()
    posts = (
        db.query(Post)
            .filter(Post.user_id == session.get('user_id'))
            .order_by(Post.created_at.desc())
            .all()
    )
    return render_template(
        'dashboard.html',
        posts=posts,
        loggedIn=session.get('loggedIn')
    )

@bp.route('/edit/<id>')
@login_required
def edit(id):
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()
    
    return render_template(
        'edit-post.html',
        post=post,
        loggedIn=session.get('loggedIn')
    )