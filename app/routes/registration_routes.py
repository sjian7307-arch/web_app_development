from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from app.models.event import Event
from app.models.registration import Registration

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/events/<int:event_id>/register', methods=['GET'])
def new_registration(event_id):
    """
    [GET] 顯示報名表單
    """
    event = Event.get_by_id(event_id)
    if not event:
        abort(404)
    
    current_registrations = Registration.count_by_event_id(event_id)
    is_full = current_registrations >= event['capacity']
    
    return render_template('registrations/new.html', event=event, is_full=is_full)

@registration_bp.route('/events/<int:event_id>/register', methods=['POST'])
def create_registration(event_id):
    """
    [POST] 接收報名資料，處理報名邏輯
    """
    event = Event.get_by_id(event_id)
    if not event:
        abort(404)
        
    current_registrations = Registration.count_by_event_id(event_id)
    if current_registrations >= event['capacity']:
        return render_template('registrations/result.html', success=False, message='活動已額滿，報名失敗。', event=event)

    participant_name = request.form.get('participant_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    if not participant_name or not email or not phone:
        flash('請填寫所有必填欄位', 'danger')
        return redirect(url_for('registration.new_registration', event_id=event_id))

    Registration.create(event_id, participant_name, email, phone)
    return render_template('registrations/result.html', success=True, message='報名成功！', event=event)

@registration_bp.route('/events/<int:event_id>/registrations', methods=['GET'])
def list_registrations(event_id):
    """
    [GET] 報名名單管理 (後台)
    """
    event = Event.get_by_id(event_id)
    if not event:
        abort(404)
        
    registrations = Registration.get_by_event_id(event_id)
    return render_template('registrations/index.html', event=event, registrations=registrations)

@registration_bp.route('/registrations/<int:registration_id>/payment', methods=['POST'])
def update_payment(registration_id):
    """
    [POST] 更新繳費狀態
    """
    registration = Registration.get_by_id(registration_id)
    if not registration:
        abort(404)
        
    payment_status = request.form.get('payment_status')
    if payment_status in ['paid', 'unpaid']:
        Registration.update_payment_status(registration_id, payment_status)
        flash('繳費狀態已更新', 'success')
        
    return redirect(url_for('registration.list_registrations', event_id=registration['event_id']))
