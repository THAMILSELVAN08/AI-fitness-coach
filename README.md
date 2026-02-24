# AI Fitness Coach

A simple web application that creates personalized fitness plans using Google's Gemini AI.

## Features

- User profile creation (name, age, weight, height, workout duration, target areas)
- AI-powered fitness plan generation using Gemini API
- Clean, responsive web interface
- Error handling for API failures
- Session-based user management

## Files

1. **main.py** - Flask web application with embedded HTML/CSS
2. **gemini_api.py** - Gemini API integration module
3. **README.md** - This file

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key

## Installation

1. **Clone or download the files**
   ```bash
   # Create a new directory
   mkdir ai-fitness-coach
   cd ai-fitness-coach
   
   # Copy the three files (main.py, gemini_api.py, README.md) to this directory
   ```

2. **Install required dependencies**
   ```bash
   pip install flask requests
   ```

3. **Get a Gemini API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Click "Get API key" and create a new API key
   - Copy the generated API key

4. **Set up environment variable**
   
   **On Windows:**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```
   
   **On macOS/Linux:**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```
   
   **Alternative: Create a .env file (recommended)**
   Create a file named `.env` in the project directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   
   Then install python-dotenv and load it in main.py:
   ```bash
   pip install python-dotenv
   ```
   
   Add this to the top of main.py (after imports):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python main.py
   ```

2. **Open your web browser**
   - Navigate to `http://localhost:5000`
   - Fill out the fitness profile form
   - Click "Generate My AI Fitness Plan" to get your personalized plan

## Usage

1. **Create Profile**: Fill in your personal details including name, age, weight, height, current workout duration, target body parts, and any additional details.

2. **Generate Plan**: After creating your profile, click the "Generate My AI Fitness Plan" button to get a personalized fitness plan from the Gemini AI.

3. **View Results**: The AI will generate a comprehensive fitness plan including:
   - Specific workout exercises with sets and reps
   - Weekly schedule recommendations
   - Nutrition guidance
   - Progression tips
   - Safety considerations

4. **Start Over**: Use the "Start Over" button to create a new profile.

## Error Handling

- If the Gemini API key is missing, you'll see: "AI Error: Gemini API key not found"
- If the API call fails, you'll see detailed error messages
- Network issues will display appropriate connection error messages

## Troubleshooting

**"Gemini API key not found" error:**
- Make sure you've set the `GEMINI_API_KEY` environment variable
- Restart your terminal/command prompt after setting the environment variable
- Verify the API key is correct and active

**"Failed to connect to Gemini API" error:**
- Check your internet connection
- Verify the API key is valid
- Make sure you haven't exceeded your API quota

**Import errors:**
- Make sure Flask and requests are installed: `pip install flask requests`
- Use Python 3.7 or higher

## Customization

- **Styling**: Modify the CSS in the `HTML_TEMPLATE` variable in `main.py`
- **Form fields**: Add or modify form fields in the HTML template and update the `/signup` route
- **AI prompts**: Customize the prompt in the `/generate-plan` route in `main.py`
- **API settings**: Adjust Gemini API parameters in `gemini_api.py`

## Security Notes

- Never commit your API key to version control
- Use environment variables or secure secret management in production
- Consider implementing rate limiting for production use
- The current setup uses a simple session-based approach suitable for development

## License

This project is provided as-is for educational and personal use.