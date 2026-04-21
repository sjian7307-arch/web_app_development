from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from app.models.event import Event

event_bp = Blueprint('event', __name__)

@event_bp.route('/')
def index():
    """
    [GET] 顯示所有活動清單
    """
    events = Event.get_all()
    return render_template('events/index.html', events=events)

@event_bp.route('/events/new')
def new_event():
    """
    [GET] 顯示建立活動表單
    """
    return render_template('events/new.html')

@event_bp.route('/events', methods=['POST'])
def create_event():
    """
    [POST] 接收表單，存入 DB，重導向至活動列表
    """
    title = request.form.get('title')
    description = request.form.get('description')
    schedule = request.form.get('schedule')
    capacity = request.form.get('capacity')
    
    if not title or not schedule or not capacity:
        flash('標題、行程表與人數上限為必填欄位', 'danger')
        return redirect(url_for('event.new_event'))
    
    try:
        capacity = int(capacity)
    except ValueError:
        flash('人數上限必須是數字', 'danger')
        return redirect(url_for('event.new_event'))

    Event.create(title, description, schedule, capacity)
    flash('活動建立成功！', 'success')
    return redirect(url_for('event.index'))

@event_bp.route('/events/<int:event_id>')
def detail(event_id):
    """
    [GET] 顯示活動詳情與行程表
    """
    event = Event.get_by_id(event_id)
    if not event:
        abort(404)
    return render_template('events/detail.html', event=event)
