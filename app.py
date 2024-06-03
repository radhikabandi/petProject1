from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Configure your OpenAI API key
openai.api_key = 'XXX'

def handle_order(order_type, details):
    # Mock API endpoint for placing an order
    # Replace with your actual order placement logic
    order_id = '12345'  # Mock order ID
    return {"status": "success", "message": f"Order placed successfully. Order ID: {order_id}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    user_input = data.get('user_input')

    # Call the OpenAI API with function calling
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        functions=[
            {
                "name": "handle_order",
                "description": "Place an order based on the user input",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_type": {
                            "type": "string",
                            "description": "Type of the order (buy or sell)"
                        },
                        "details": {
                            "type": "string",
                            "description": "Details of the order"
                        }
                    },
                    "required": ["order_type", "details"]
                }
            }
        ],
        function_call="auto"
    )

    # Extract the order_type and details from the response
    message = response.choices[0].message
    function_call = message.get('function_call')
    if function_call and function_call['name'] == 'handle_order':
        args = function_call['arguments']
        order_type = args.get('order_type')
        details = args.get('details')
        result = handle_order(order_type, details)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "Unable to process the order."})

if __name__ == '__main__':
    app.run(debug=True)
