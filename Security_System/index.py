# L9HWKL425V53MGE5ST3PU9K1
import cv2
from twilio.rest import Client

account_sid = 'TWILIO_ACCOUNT_SID'        # Replace with your Twilio Account SID
auth_token = 'TWILIO_AUTH_TOKEN'          # Replace with your Twilio Auth Token
client = Client(account_sid, auth_token)

# Twilio configuration
def send_sms(body):
    message = client.messages.create(
        body=body,
        from_='TWILIO_PHONE_NUMBER',  # Replace with your Twilio phone number
        to='RECIPIENT_PHONE_NUMBER'      # Replace with the recipient's phone number
    )
    
    if message.sid:
        print("SMS sent successfully")
    else:
        print("Failed to send SMS")

# Load pre-trained model
cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
body_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(bodies) > 0:
        send_sms("Motion detected in front of the camera!")
    
    # Draw rectangles around detected bodies
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    cv2.imshow('Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
