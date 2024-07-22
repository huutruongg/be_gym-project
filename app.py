from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.calculator import calculate_bmr, calculate_tdee, calculate_calories
from modules.diet_generator import generate_diet_plan
from models import db, Blog, InstructionalVideo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)  
CORS(app)
# Meal plan routes
@app.route('/get_diet_plan', methods=['POST'])
def get_diet_plan():
    data = request.json
    gender = data['gender']
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    intensity = data['intensity']
    goal = data['goal']
    level = data['level']
    expected = data.get('expected', '') 
    print(data)
    # result
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, intensity)
    calories = calculate_calories(tdee, goal)
    meal_plan = generate_diet_plan(gender, age, height, weight, intensity, goal, level, expected, tdee, calories)
    return jsonify({'bmr': bmr, 'tdee': tdee, 'calories': calories, 'meal_plan': meal_plan})

# Blog routes
@app.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_dict())

@app.route('/blogs', methods=['POST'])
def create_blog():
    data = request.json
    new_blog = Blog(imageURL=data['imageURL'], author=data['author'], title=data['title'], content=data['content'])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({'message': 'Blog created!', 'id': new_blog.id}), 201

@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    blog.imageURL = data.get('imageURL', blog.imageURL)
    blog.author = data.get('author', blog.author)  
    blog.title = data.get('title', blog.title)
    blog.content = data.get('content', blog.content)
    db.session.commit()
    return jsonify({'message': 'Blog updated!'})

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted!'})


# Video routes
@app.route('/guides', methods=['GET'])
def get_guides():
    guides = InstructionalVideo.query.all()
    return jsonify([guide.to_dict() for guide in guides])

@app.route('/guides/<int:guide_id>', methods=['GET'])
def get_guide(guide_id):
    guide = InstructionalVideo.query.get_or_404(guide_id)
    return jsonify(guide.to_dict())

@app.route('/guides', methods=['POST'])
def create_guide():
    if request.content_type == 'application/json':
        data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded' or request.content_type == 'multipart/form-data':
        data = request.form
    elif request.args:
        data = request.args
    else:
        return jsonify({'message': 'Unsupported Media Type'}), 415

    new_guide = InstructionalVideo(
        author=data.get('author'),
        title=data.get('title'),
        url_video=data.get('url_video')
    )
    db.session.add(new_guide)
    db.session.commit()
    return jsonify({'message': 'Guide created!', 'id': new_guide.id}), 201

@app.route('/guides/<int:guide_id>', methods=['PUT'])
def update_guide(guide_id):
    guide = InstructionalVideo.query.get_or_404(guide_id)
    data = request.json
    guide.author = data.get('author', guide.author)  
    guide.title = data.get('title', guide.title)
    guide.url_video = data.get('url_video', guide.url_video)
    db.session.commit()
    return jsonify({'message': 'Guide updated!'})

@app.route('/guides/<int:guide_id>', methods=['DELETE'])
def delete_guide(guide_id):
    guide = InstructionalVideo.query.get_or_404(guide_id)
    db.session.delete(guide)
    db.session.commit()
    return jsonify({'message': 'Guide deleted!'})

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()
    app.run(debug=True)