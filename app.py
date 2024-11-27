from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
CORS(app, origins=["https://mediahope.ru"])

# Пути к файлам
BASE_DIR = os.path.abspath(".")
FONT_BOLD = os.path.join(BASE_DIR, "data/Montserrat-Bold.ttf")
FONT_MEDIUM = os.path.join(BASE_DIR, "data/Montserrat-Medium.ttf")
OBJECT_SANS = os.path.join(BASE_DIR, "data/ObjectSans-Heavy.ttf")
PATTERNS = [
    os.path.join(BASE_DIR, "data/pattern.jpg"),
    os.path.join(BASE_DIR, "data/pattern-1.jpg"),
    os.path.join(BASE_DIR, "data/pattern-2.jpg"),
    os.path.join(BASE_DIR, "data/pattern-3.jpg"),
    os.path.join(BASE_DIR, "data/pattern-4.jpg"),
    os.path.join(BASE_DIR, "data/pattern_aw.jpg"),
]

@app.route("/", methods=["GET"])
def form():
    return '''
    <form method="POST" action="/generate" enctype="multipart/form-data">
        Имя: <input type="text" name="name" /><br>
        Дата: <input type="text" name="date" /><br>
        Время: <input type="text" name="time" /><br>
        Фон:
        <input type="radio" name="background" value="0" checked> Шаблон 1
        <input type="radio" name="background" value="1"> Шаблон 2
        <input type="radio" name="background" value="2"> Шаблон 3
        <input type="radio" name="background" value="3"> Шаблон 4
        <input type="radio" name="background" value="4"> Шаблон 5
        <input type="radio" name="background" value="5"> Another World<br>
        <button type="submit">Сгенерировать</button>
    </form>
    '''

@app.route("/generate", methods=["POST"])
def generate():
    # Получаем данные из формы
    name = request.form.get("name", "").upper()
    date = request.form.get("date", "").upper()
    time = request.form.get("time", "").upper()
    background = int(request.form.get("background", 0))

    # Открываем шаблон
    img = Image.open(PATTERNS[background])
    draw = ImageDraw.Draw(img)
    
    # Настраиваем шрифты
    if background == 5:  # Шаблон "Another World"
        font_name = ImageFont.truetype(OBJECT_SANS, size=67)
        date_time_text = f"{date} {time}"
        draw.text((131, 1365), name, font=font_name, fill="#e3000f")
        draw.text((663 - draw.textlength(date_time_text, font=font_name) // 2, 760), date_time_text, font=font_name, fill="white")
    else:
        font_name = ImageFont.truetype(FONT_BOLD, size=200)
        font_date = ImageFont.truetype(FONT_MEDIUM, size=200)
        font_time = ImageFont.truetype(FONT_MEDIUM, size=200)

        # Наложение текста
        draw.text((256, 1200), date, font=font_date, fill="white")
        draw.text((256, 1439), time, font=font_time, fill="white")
        text_width = draw.textlength(name, font=font_name)
        draw.text((img.width - text_width - 105, 2527), name, font=font_name, fill="white")

    # Сохраняем результат
    output_path = os.path.join(BASE_DIR, "output.jpg")
    img.save(output_path)

    # Возвращаем файл пользователю
    return send_file(output_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
