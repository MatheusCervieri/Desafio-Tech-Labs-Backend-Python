from flask import Blueprint, render_template

documentation_bp = Blueprint('documentation', __name__)

@documentation_bp .route('/documentacao', methods=['GET'])
def pagina_teste():
    return render_template('documentation.html')