from flask import Flask , request , jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/" , methods =["GET"])
def home():
    return jsonify({"messaga" : "Welcome to the PPT Generator !"})

@app.route("/generate" , methods = ["POST"])
def generate():
    return jsonify({"message" : "generate the ppt with this Topic,number of slides , select the ppt layout of ppt in a list,Tone/Style,Depth of Content,Theme/Color"})

@app.route("/preview/<ppt>")#Temporary route 
def preview_pptx(ppt : str):
    return jsonify({"message" : f"Preview the ppt idk {ppt}"})

@app.route("/download/<ppt>")
def dowmload(ppt):
    return jsonify({"message" : "Down the ppt"})

if __name__ == "__main__":
    app.run(debug=True)