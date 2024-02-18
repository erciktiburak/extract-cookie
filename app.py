from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_cookies', methods=['POST'])
def extract_cookies():
    domain = request.form['domain']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    cookie_name = request.form['cookie_name']

    # Call your extract_cookies function with the provided parameters
    # extract_cookies(domain=domain, start_date=start_date, end_date=end_date, cookie_name=cookie_name)

    return jsonify({'message': 'Cookies extracted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)