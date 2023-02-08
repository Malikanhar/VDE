FROM python:3.8-slim

RUN mkdir /vibrio_detector_app
COPY streamlit_app/ /vibrio_detector_app/

RUN pip install \
    pillow \
    opencv-python-headless \
    streamlit

EXPOSE 8501

CMD [ "streamlit", "run", "/vibrio_detector_app/vibrio_detector_app.py" ]
