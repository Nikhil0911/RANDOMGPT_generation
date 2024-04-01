from flask import Flask, render_template, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_code():
    description = request.form['description']
    
    # Tokenize the description
    input_ids = tokenizer.encode(description, return_tensors="pt")
    
    # Generate code based on the description
    output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2, top_k=10, top_p=0.95, temperature=0.7)
    
    # Decode the generated code
    generated_code = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return render_template('result.html', description=description, generated_code=generated_code)

if __name__ == '__main__':
    app.run(debug=True)
