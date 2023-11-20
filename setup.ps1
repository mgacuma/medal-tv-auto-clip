# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate # On Mac

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment when done (optional)
deactivate