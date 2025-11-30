from flask import Blueprint, session, redirect, request

language_bp = Blueprint('language', __name__)


@language_bp.route('/set/<lang>')
def set_language(lang):
    if lang in ['en', 'bg']:
        session['language'] = lang

    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect('/')
