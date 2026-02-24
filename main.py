from flask import Flask, render_template_string, request, jsonify, session
import os
from gemini_api import call_gemini

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Fitness Coach</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        
        .hero {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .hero h1 {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .hero p {
            color: #666;
            font-size: 1.2rem;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: #6c757d;
            margin-right: 15px;
            width: auto;
        }
        
        .profile-info {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        
        .profile-info h3 {
            color: #495057;
            margin-bottom: 15px;
        }
        
        .profile-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .profile-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .profile-item strong {
            color: #333;
        }
        
        .fitness-plan {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 25px;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #dc3545;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not session.get('user_profile') %}
        <!-- Fitness Form -->
        <div class="card">
            <div class="hero">
                <h1>🏋️ AI Fitness Coach</h1>
                <p>Get your personalized fitness plan powered by AI</p>
            </div>
            
            <form method="POST" action="/signup">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Full Name</label>
                        <input type="text" id="name" name="name" required placeholder="Enter your full name">
                    </div>
                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" name="age" required placeholder="Your age" min="13" max="100">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="weight">Weight (kg)</label>
                        <input type="number" id="weight" name="weight" required placeholder="Weight in kg" min="30" max="300">
                    </div>
                    <div class="form-group">
                        <label for="height">Height (cm)</label>
                        <input type="number" id="height" name="height" required placeholder="Height in cm" min="100" max="250">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="dailyWorkout">Current Daily Workout Duration</label>
                    <select id="dailyWorkout" name="dailyWorkout" required>
                        <option value="">Select workout duration</option>
                        <option value="No workout">No workout currently</option>
                        <option value="15-30 minutes">15-30 minutes</option>
                        <option value="30-45 minutes">30-45 minutes</option>
                        <option value="45-60 minutes">45-60 minutes</option>
                        <option value="1+ hours">1+ hours</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="targetBodyPart">Target Body Part to Improve</label>
                    <select id="targetBodyPart" name="targetBodyPart" required>
                        <option value="">Select target area</option>
                        <option value="Full body">Full body</option>
                        <option value="Upper body">Upper body</option>
                        <option value="Lower body">Lower body</option>
                        <option value="Core/Abs">Core/Abs</option>
                        <option value="Arms">Arms</option>
                        <option value="Legs">Legs</option>
                        <option value="Back">Back</option>
                        <option value="Chest">Chest</option>
                        <option value="Cardio fitness">Cardio fitness</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="otherDetails">Additional Details</label>
                    <textarea id="otherDetails" name="otherDetails" placeholder="Any injuries, fitness goals, preferences, or other relevant information..."></textarea>
                </div>
                
                <button type="submit" class="btn">Create My Fitness Profile</button>
            </form>
        </div>
        
        {% else %}
        <!-- Dashboard -->
        <div class="card">
            <div class="hero">
                <h1>Welcome, {{ session.user_profile.name }}! 👋</h1>
                <p>Your AI Fitness Coach is ready to help you achieve your goals</p>
            </div>
            
            <div class="profile-info">
                <h3>📋 Your Profile Summary</h3>
                <div class="profile-grid">
                    <div class="profile-item">
                        <strong>Age:</strong> {{ session.user_profile.age }} years
                    </div>
                    <div class="profile-item">
                        <strong>Weight:</strong> {{ session.user_profile.weight }} kg
                    </div>
                    <div class="profile-item">
                        <strong>Height:</strong> {{ session.user_profile.height }} cm
                    </div>
                    <div class="profile-item">
                        <strong>Current Workout:</strong> {{ session.user_profile.dailyWorkout }}
                    </div>
                    <div class="profile-item">
                        <strong>Target Area:</strong> {{ session.user_profile.targetBodyPart }}
                    </div>
                    {% if session.user_profile.otherDetails %}
                    <div class="profile-item">
                        <strong>Additional Details:</strong> {{ session.user_profile.otherDetails }}
                    </div>
                    {% endif %}
                </div>
            </div>
            
            <form method="POST" action="/generate-plan">
                <button type="submit" class="btn" {% if generating %}disabled{% endif %}>
                    {% if generating %}
                    🤖 Generating Your AI Fitness Plan...
                    {% else %}
                    🚀 Generate My AI Fitness Plan
                    {% endif %}
                </button>
            </form>
            
            {% if generating %}
            <div class="loading">
                <div class="spinner"></div>
                <p>Our AI is creating your personalized fitness plan...</p>
            </div>
            {% endif %}
            
            {% if error %}
            <div class="error">
                <strong>AI Error:</strong> {{ error }}
            </div>
            {% endif %}
            
            {% if fitness_plan %}
            <div class="fitness-plan">
                <h3>🎯 Your Personalized Fitness Plan</h3>
                {{ fitness_plan }}
            </div>
            {% endif %}
            
            <form method="POST" action="/reset" style="margin-top: 20px;">
                <button type="submit" class="btn btn-secondary">← Start Over</button>
            </form>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/signup', methods=['POST'])
def signup():
    user_profile = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'weight': request.form.get('weight'),
        'height': request.form.get('height'),
        'dailyWorkout': request.form.get('dailyWorkout'),
        'targetBodyPart': request.form.get('targetBodyPart'),
        'otherDetails': request.form.get('otherDetails', '')
    }
    
    session['user_profile'] = user_profile
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    if 'user_profile' not in session:
        return render_template_string(HTML_TEMPLATE, error="Please create your profile first.")
    
    try:
        profile = session['user_profile']
        
        # Create prompt for Gemini API
        prompt = f"""Create a detailed, personalized fitness plan for:

Name: {profile['name']}
Age: {profile['age']} years
Weight: {profile['weight']} kg
Height: {profile['height']} cm
Current workout duration: {profile['dailyWorkout']}
Primary focus area: {profile['targetBodyPart']}
Additional details: {profile['otherDetails'] or 'None'}

Please provide:
1. **WORKOUT PLAN**: Specific exercises with sets, reps, and rest periods
2. **WEEKLY SCHEDULE**: How many days per week and which days
3. **NUTRITION GUIDANCE**: Basic dietary recommendations 
4. **PROGRESSION TIPS**: How to advance over time
5. **SAFETY NOTES**: Important considerations based on their profile

Make it practical, achievable, and motivating. Format with clear sections and bullet points."""

        # Call Gemini API
        fitness_plan = call_gemini(prompt, profile)
        
        return render_template_string(HTML_TEMPLATE, fitness_plan=fitness_plan)
        
    except Exception as e:
        error_message = str(e)
        return render_template_string(HTML_TEMPLATE, error=error_message)

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)