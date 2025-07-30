import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_voting_secret_key")

# In-memory vote storage using global variables
vote_counts = {
    'cats': 0,
    'dogs': 0
}

@app.route('/')
def index():
    """Display the main voting page with current vote counts."""
    return render_template('index.html', vote_counts=vote_counts)

@app.route('/vote', methods=['POST'])
def vote():
    """Handle vote submission."""
    choice = request.form.get('choice')
    
    # Validate the vote choice
    if choice not in ['cats', 'dogs']:
        flash('Invalid vote choice. Please select either Cats or Dogs.', 'error')
        return redirect(url_for('index'))
    
    # Record the vote
    vote_counts[choice] += 1
    
    # Show confirmation message
    choice_display = choice.capitalize()
    flash(f'Thank you for voting for {choice_display}! Your vote has been recorded.', 'success')
    
    # Log the vote for debugging
    app.logger.info(f'Vote recorded for {choice}. Current counts: {vote_counts}')
    
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_votes():
    """Reset all vote counts to zero."""
    global vote_counts
    vote_counts = {'cats': 0, 'dogs': 0}
    flash('Vote counts have been reset!', 'info')
    app.logger.info('Vote counts reset')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
