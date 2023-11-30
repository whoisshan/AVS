from flask import Flask, request, jsonify, render_template
from flask_basicauth import BasicAuth
import pandas as pd

app = Flask(__name__)

# Basic Auth Configuration
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'pass123'
basic_auth = BasicAuth(app)

# Read data from Excel sheet
df = pd.read_excel('Addreses.xlsx')
# print("Here")
# print(df.head(10))

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def find_matching_address(user_address):
    # Logic to find a matching address in the dataframe
    for index, row in df.iterrows():
        if row["Street Address"] == user_address["addressLine1"] and \
           row["City"] == user_address["city"] and \
           row["State"] == user_address["stateProv"] and \
           row["ZipCode"] == user_address["postalCode"]:
            return {
                "firstName": "", 
                "lastName": "",  
                **user_address
            }
    return None

@app.route('/verifyAddress', methods=['POST'])
@basic_auth.required
def verify_address():
    try:
        user_address = request.json.get('Address')
        matched_address = find_matching_address(user_address)

        if matched_address:
            response = {
                "avsAddressDetails": {
                    "responseStatus": True,
                    "addressVerified": True,
                    "avsResponseCode": 100,
                    "avsResponseDecision": "Success",
                    "address": user_address,
                    "recommendedAddresses": {
                        "recommendedAddress": matched_address
                    }
                }
            }
        else:
            response = {
                "avsAddressDetails": {
                    "responseStatus": True,
                    "addressVerified": False,
                    "avsResponseCode": 100,
                    "avsResponseDecision": "Failure",
                    "address": user_address
                }
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
