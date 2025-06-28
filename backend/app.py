from flask import Flask , request , jsonify
from flask_cors import CORS
from model.model import MyModel
from ppt_layouts.ppt_layouts import ppt
app = Flask(__name__)
CORS(app)

@app.route("/" , methods =["GET"])
def home():
    return jsonify({"message" : "Welcome to the PPT Generator !"})

@app.route("/generate" , methods = ["POST"])
def generate():
    '''
    data = {
    "topic" : "",
    "slides" : int,
    "layout" : int # lets build slowly,
    "tone" : "", #lets build slowly,
    "depth" : "", # lets build slowly,
    "color_scheme" : ["" ,""] # lets build slowly, background and text color 
    }
    '''
    data = request.get_json()
    
    # Check if data is None or missing required fields
    if not data:
        return jsonify({"error": "No JSON data provided"})
    
    if 'topic' not in data or 'slides' not in data:
        return jsonify({"error": "Missing required fields: 'topic' and 'slides'"})
    
    llm = MyModel()
    ppt_obj = ppt()

    topic = data['topic']
    no_of_slides = data['slides']
    layout = data['layout']
    tone = data['tone']
    depth = data['depth']
    color_scheme = data['color_scheme']
    font_style = data['font_style']
    try :
        list_of_topics =  llm.generate_title_of_slides(topic ,(no_of_slides))
        list_of_content = llm.generate_content_of_topics(subtopics =list_of_topics , tone=tone , depth=depth)
        response = ppt_obj.generate_ppt(topic , list_of_content , list_of_topics , no_of_slides , color_scheme , font_style)
        return jsonify({"message" : list_of_topics , "content" : list_of_content  , "status" : response })
    except Exception as e:
        return jsonify({"message" : f"Error Errored in /generate error ;- {e}"})

@app.route("/preview/<ppt>")#Temporary route 
def preview_pptx(ppt : str):
    return jsonify({"message" : f"Preview the ppt idk {ppt}"})

@app.route("/download/<ppt>")
def download(ppt):
    return jsonify({"message" : "Down the ppt"})

if __name__ == "__main__":
    app.run(debug=True)