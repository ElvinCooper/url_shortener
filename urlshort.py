from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/mi-url', methods=['GET', 'POST'])
def mi_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('Este nombre ya existe para una URL, porfavor elija uno diferente')
            return redirect(url_for('urlshort.home'))
        
        # validando datos para cargar archivos
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}

        elif 'file' in request.files.keys():
            f = request.files['file']            
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:\\Users\\ecooper\\Documents\\flask_projects\\url_shortener\\urlshort\\static\\user_files\\' + full_name)
            urls[request.form['code']] = {'file':full_name}
        else:
            flash('Debe cargar u archivo y su respectiva descripcion')

       # urls[request.form['code']] = {'url':request.form['url']} 
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('mi_url.html', codigo = request.form['code'])  
    else:
        return redirect(url_for('urlshort.home'))
    
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404) #"URL no encontrada", 404
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

if bp == '__main__':
    bp.run(debug=True)
