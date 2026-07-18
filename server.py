from flask import Flask, render_template, request 
from EmotionDetection.emotion_detection import emotion_detector
import json

app = Flask("Emotion Detection")

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/emotionDetector") 
def sent_analyzer(): 
    """
    Obtiene lso datos de emociones
    """
    # Recuperar el texto a analizar de los argumentos de la solicitud 
    text_to_analyze = request.args.get('textToAnalyze')
    # Pasar el texto a la función emotion_detector y almacenar la respuesta 
    response = emotion_detector(text_to_analyze)
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again."
    
    # 1. Extraemos la emoción dominante
    dominant = response.get('dominant_emotion')
    
    # 2. Creamos una lista de los puntajes formateados para que se vean bonitos
    # Excluimos 'dominant_emotion' del bucle para no mostrarla en la lista
    emotions_list = []
    for key, value in response.items():
        if key != 'dominant_emotion':
            emotions_list.append(f"'{key}': {value}")
    
    # Unimos todo con comas, excepto el último que lleva un 'and'
    emotions_str = ", ".join(emotions_list[:-1]) + " and " + emotions_list[-1]
    
    # 3. Construimos el mensaje final
    result = f"For the given statement, the system response is {emotions_str}. 
    result += f"The dominant emotion is {dominant}."
    
    return result

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)
