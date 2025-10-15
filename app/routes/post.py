from flask import Blueprint, abort, render_template, request, redirect
from flask_login import current_user, login_required

from ..forms import StudentForm, TeacherForm
from ..extensions import db
from ..models.post import Post
from ..models.user import User


post = Blueprint('post', __name__)


@post.route('/', methods=['POST', 'GET'])
def all():
    form = TeacherForm()
    form.teacher.choices = [(t.id, t.name) for t in User.find_by_status('teacher')]

    if request.method == 'POST':
        teacher_id = form.teacher.data
        posts = Post.get_by_teacher(teacher_id)
    else:
        posts = Post.get_all_oredered_by_date(True)

    return render_template('post/all.html', posts=posts, user=User, form=form)


@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = StudentForm()
    form.student.choices = [(s.id, s.name) for s in User.find_by_status('user')]
    if request.method == 'POST':
        subject = request.form['subject']
        student_id = form.student.data
        try:
            Post.create_post(teacher=current_user.id, subject=subject, student=student_id)
            return redirect('/')
        except Exception as e:
            print(str(e))

    return render_template('post/create.html', form=form)


@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Post.get_by_id(id)

    if post.author.id == current_user.id:
        form = StudentForm()
        form.student.choices = [(s.id, s.name) for s in User.find_by_status('user')]
        
        if request.method == 'GET':
            form.student.data = post.student
        
        if request.method == 'POST':
            subject = request.form['subject']
            student_id = form.student.data
            try:
                Post.update_post(post, subject=subject, student=student_id)
                return redirect('/')
            except Exception as e:
                print(str(e))
    else:
        abort(403)
        
    return render_template('post/update.html', post=post, form=form)
    

@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.get_by_id(id)

    if post.author.id == current_user.id:
        try:
            Post.delete_post(id)
        except Exception as e:
            print(str(e))
        return redirect('/')
    else:
        abort(403)


        