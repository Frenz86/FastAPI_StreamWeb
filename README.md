# FastAPI_StreamWeb

Questo stremaerAPI è un po pazziarello, ha un routing interno ovvero:

lo stremaer (python o javascript) mandera le immagini webcam in formato base64 ascii binario con metodo POST all'API  --> /send_frame_from_file/{img_id}
  questo internamente lo routerà in GET all "/video_feed/{img_id}" sul html 127.0.0.1:8000, 

per il test con python:
- pip install -r requirements.txt
- python main.py

in un secondo terminale:
- streamlit run app.py  
(si aprirà il client streamer sulla 8501) -- > selezionare la spunta da camere + API

a questo punto se andiamo su html 127.0.0.1:8000 vedremo il nostro bel faccione :=)

Cosa manca?
Bisognerebbe fare lo streamer (che in questo caso è fatto in python con streamlit con javascript, poichè poi potrei inserire tutto
il rpogetto all'interno di un docker)

