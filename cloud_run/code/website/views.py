from flask import Blueprint, render_template, request

def remove_line_breaks(input):
    # Split the input into lines and strip trailing whitespace from each line
    lines = [line.rstrip('\r\n') for line in input.splitlines()]
    # Combine the lines back into input with newline separators
    user_input = ' '.join(lines)
    cleaned_input = user_input.replace('\\', '')
    return cleaned_input


views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        cleaned_input = remove_line_breaks(user_input)
        return render_template("home.html", cleaned_input=cleaned_input)
    return render_template("home.html")

@views.route("/about")
def about():
    return render_template("about.html")
