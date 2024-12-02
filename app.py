from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/postgres'
db = SQLAlchemy(app)

class Respondent(db.Model):
    __tablename__ = 'respondents'  # Убедитесь, что здесь указано правильное имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    respondent = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)

@app.route('/getPercent', methods=['GET'])
def get_percent():
    audience1_filter = request.args.get('audience1')
    audience2_filter = request.args.get('audience2')

    # Получаем данные для первой аудитории
    audience1 = db.session.query(
        Respondent.respondent,
        db.func.avg(Respondent.weight).label('avg_weight')
    ).filter(text(audience1_filter)).group_by(Respondent.respondent).all()

    # Получаем данные для второй аудитории
    audience2 = db.session.query(
        Respondent.respondent,
        db.func.avg(Respondent.weight).label('avg_weight')
    ).filter(text(audience2_filter)).group_by(Respondent.respondent).all()

    audience1_weights = {resp[0]: resp[1] for resp in audience1}
    audience2_weights = {resp[0]: resp[1] for resp in audience2}
    print(audience1_weights)
    print(audience2_weights)
    # Вычисляем общий вес обеих аудиторий
    total_weight_audience1 = sum(audience1_weights.values())
    total_weight_audience2 = sum(audience2_weights.get(resp, 0) for resp in audience1_weights.keys())

    if total_weight_audience1 == 0:
        return jsonify({'percent': 0})

    percent = total_weight_audience2 / total_weight_audience1
    return jsonify({'percent': round(percent*100, 3)})

if __name__ == '__main__':
    app.run(debug=True)

