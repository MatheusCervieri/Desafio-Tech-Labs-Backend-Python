from flask import Blueprint, render_template

teste_bp = Blueprint('teste', __name__)

@teste_bp.route('/teste', methods=['GET'])
def pagina_teste():
    return render_template('teste.html')