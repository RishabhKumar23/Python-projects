import cv2
import cvzone
import socket
import struct
import pickle
from cvzone.FaceMeshModule import FaceMeshDetector

# Initialize FaceMesh detector with a maximum of 1 face
detector = FaceMeshDetector(maxFaces=1)

# Connect to Raspberry Pi server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("raspberrypi.local", 9999))  # Change to Pi's IP if needed

data = b""
payload_size = struct.calcsize("Q")  # Size of the packed message size

while True:
    # Retrieve message size
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]  # Unpack message size

    # Retrieve the actual frame data
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize frame
    img = pickle.loads(frame_data)

    # Process with FaceMesh detector
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]  # Left eye landmark
        pointRight = face[374]  # Right eye landmark

        # Distance Calculation
        w, _ = detector.findDistance(pointLeft, pointRight)  # Distance between eyes in pixels
        W = 6.3  # Average human eye distance in cm
        f = 940  # Predefined focal length
        d = (W * f) / w  # Compute distance
        print(f"Depth: {int(d)}cm")

        # Overlay Depth Info
        cvzone.putTextRect(img, f'Depth: {int(d)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)

    # Display the frame
    cv2.imshow("Stream from Raspberry Pi", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and destroy all windows
client_socket.close()
cv2.destroyAllWindows()
