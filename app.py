from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fooddatabase.db'
app.config['SQLALCHEMY_BINDS'] = {'goal':'sqlite:///goaldatabase.db'}


db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Goal(db.Model):

    __bind_key__ = 'goal'

    id = db.Column(db.Integer, primary_key=True)

    calorie_goal = db.Column(db.Integer)
    fat_goal = db.Column(db.Integer)
    protein_goal = db.Column(db.Integer)
    carbs_goal = db.Column(db.Integer)


@app.route('/', methods=['POST', 'GET'])
def index():

    user_calories_goal = 0
    user_f_goal = 0
    user_p_goal = 0
    user_carbs_goal = 0
    

    if request.method == "POST":

        if 'food-log' in request.form:

            food_content = request.form['food']
            calories_content = request.form['calories']
            fat_content = request.form['fat']
            protein_content = request.form['protein']
            carbs_content = request.form['carbs']

            new_user = User(food=food_content, calories=calories_content, fat=fat_content, protein=protein_content, carbs=carbs_content)

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')

            except:
                return "There was an issue !"

        else:
 
            user_calories_goal = request.form['calorie-goal']
            user_f_goal = request.form['fat-goal']
            user_p_goal = request.form['protein-goal']
            user_carbs_goal = request.form['carbs-goal']

            new_goal = Goal(calorie_goal=user_calories_goal, fat_goal=user_f_goal, protein_goal=user_p_goal, carbs_goal=user_carbs_goal)

            try:
                db.session.add(new_goal)
                db.session.commit()
                return redirect('/')

            except:
                return "There was an issue !"

    else:
        

        items = User.query.order_by(User.date_created).all()
        goals = Goal.query.all()
        ccal = 0
        cf = 0
        cp = 0
        cc = 0

        if not items:
            print('list empty')
        else:
            for i in items:
                ccal += float(i.calories)
                cf += float(i.fat)
                cp += float(i.protein)
                cc += float(i.carbs)


        if not goals:
            goals.append(Goal(calorie_goal=user_calories_goal, fat_goal=user_f_goal, protein_goal=user_p_goal, carbs_goal=user_carbs_goal))


        return render_template('index.html', items = items, goals = goals[-1], ccal = ccal, cf = cf, cp = cp, cc = cc)

@app.route('/reset')
def reset():

    items = User.query.order_by(User.date_created).all()
    goals = Goal.query.all()
    
    for i in range(1, len(items)+1):

        try:
            db.session.delete(User.query.get_or_404(i))
            db.session.commit()

        except:
            return "Error in resetting"



    for i in range(1, len(goals)+1):
        
        try:
            db.session.delete(Goal.query.get_or_404(i))
            db.session.commit()

        except:
            return "Error in resetting"

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    delete_item = User.query.get_or_404(id)

    try:
        db.session.delete(delete_item)
        db.session.commit()
        return redirect('/')

    except:

        return "Sorry an error has occured"



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    item = User.query.get_or_404(id)
    

    if request.method =='POST':
        
        item.food = request.form['food']
        item.calories = request.form['calories']
        item.fat = request.form['fat']
        item.protein = request.form['protein']
        item.carbs = request.form['carbs']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return "an issue occured"

    else:
        return render_template('update.html', item=item)



if __name__ == '__main__':
    app.run(debug=True)


