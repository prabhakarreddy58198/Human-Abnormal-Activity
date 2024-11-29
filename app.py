import streamlit as st
import vid_pred
import cv2
import shutil
import os
import helper
import beepy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

frame_th = 50
helper.del_dir('temp')

def save_video(video_file):
    with open("uploaded_video.mp4", "wb") as f:
        f.write(video_file.read())
    return "uploaded_video.mp4"

def read_video(path):
    video_file = open(path, 'rb')
    video_bytes = video_file.read()
    return video_bytes

def send_email(subject, body, attachment_path=None):
    sender_email = 'krishnakc225r@gmail.com'
    sender_password = 'rupo lnwr epcf wgrc'
    receiver_email = 'udaylabb3@gmail.com'
    
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(attachment_path))
        message.attach(part)

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())
    smtp_server.quit()


CLASSES_LIST = ['Arson', 'Normal', 'Vandalism', 'Arrest', 'Abuse', 'Assault', 'Explosion', 'Fighting', 'Shooting', 'Stealing', 'RoadAccidents', 'Robbery', 'Shoplifting', 'Burglary']

st.title('Anomaly detection app')
choice = st.sidebar.radio(label='Select', options=['Upload'])

if choice == 'Upload':
    video_file = st.file_uploader("Upload video", type=["mp4"])
    if st.button('Predict'):
        if video_file is not None:
            vid_path = save_video(video_file)
            video_bytes = read_video(vid_path)
            st.video(video_bytes)
            pred, prob = vid_pred.vid_class_pred(vid_path, CLASSES_LIST)
            
            st.markdown(f'Prediction class: {pred}')
            st.markdown(f'Prediction prob: {prob}')
            
            if pred != 'Normal':
                if prob > 0.8 :
                    beepy.beep(sound='error')
                if prob >0.8:
                    send_email('Anomaly detected', f'Anomaly detected in the video. Class: {pred}, Probability: {prob}', attachment_path=vid_path)
                else:
                    send_email('Anomaly detected', f'Anomaly detected in the video. Class: {pred}, Probability: {prob}', attachment_path=vid_path)
            else:
                send_email('Normal video', f'. Class: {pred}, Probability: {prob}', attachment_path=vid_path)
        else:
            st.error('Video file not uploaded')
# elif choice == 'Display Images':
#     display_images()
# else:
#     pass
