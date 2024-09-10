import picamera2
import numpy as np
from time import sleep 
import cv2
import serial
import torch
from PIL import Image
from my_model import my_model
from command import ArduinoCommand
from torchvision.utils import draw_bounding_boxes
from torchvision import transforms

def take_one_photo_and_predict():
    # Initialize the camera
    camera = picamera2.Picamera2()
    camera_config = camera.create_still_configuration({"size": (3280 , 2464)})  # Example resolution, adjust based on your camera's specs
    camera.configure(camera_config)
    camera.start()

    # Preprocess function (you'll need to define this)


    # Send the "leds_up" command to Arduino via serial communication
    # arduino_port = "/dev/ttyACM0"  # Adjust the port name as needed
    # ser = serial.Serial(arduino_port, baudrate=9600, timeout=1)
    # ser.write(b"leds_up")  # Send the command
    sleep(2)  # Wait for 2 seconds
    model = my_model.get_model_instance_segmentation(3)
    # Load the PyTorch model from the .pth file
    device = torch.device('cpu')

    checkpoint = torch.load('checkpoint_after_(6).pth',map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    # Class names (adjust as needed)
    class_names = ["background", "fertile", "unfertile"]

    # Capture images and make predictions

    # Send the "move_x" command to Arduino
    # ser.write(f"move_to_({x})".encode())
    sleep(2)  # Wait for 2 seconds after each movement

    # Initialize an empty list to store frames
    frames = []
    target = {}
    i=0
    transform = transforms.Compose([
        # transforms.Resize((2048, 2048)),  # Resize the image to the size expected by the model
        transforms.ToTensor(),  # Convert the image to a PyTorch tensor
        ])
    # Capture multiple frames
    for i in range(1, 6):
        frame = camera.capture_image("main")
        frame = frame.resize((2048,2048)).convert("RGB")
        # ser.write(b"move_little")
        frame.save(f"sample_of_move_{0}_number_{i}.jpg")
        frame = transform(frame).unsqueeze(0).to(device)
        print(frame.shape)
        # frame = np.array(frame)
        frames.append(frame)  # Store the frame in the list

        

        # Convert the processed frame to a PyTorch tensor
    input_tensors = frames
    output_final = 0
        
    for j,input_tensor in enumerate(input_tensors) :

            # Make predictions
            with torch.no_grad():
                output = model(input_tensor)

            # Interpret the output
            max_score = output[0]['scores'].max().item()
            max_score_idx = output[0]['scores'].argmax().item()
            max_score_label = output[0]['labels'][max_score_idx].item()
            max_score_box = output[0]['boxes'][max_score_idx].unsqueeze(0).cpu()
            print(max_score_box)
            print(j,"----->",max_score_label)

            if max_score_label == 1:
                output_final += 1  
                print('+1')
            if output_final >=3 :
                color = "green"
                label = 1
                print('breaking ')
                break 
            
    # Decision based on label
    if output_final < 3:
        # Send "move_unfertile" command to Arduino
        # ser.write(b"move_to_(11)")
        label = 2
        color = "red"
        sleep(4)  # Delay 4 seconds
        
            
    uint8_image = (frame * 255).to(torch.uint8).squeeze(0)

    # Get the corresponding bbox
    output_image = draw_bounding_boxes(uint8_image, max_score_box,
                                        labels=[f"{class_names[label]}: {max_score:.3f}"],
                                        colors = color,
                                        font = 'ARIAL.TTF' ,font_size = 100)
        
        # Save the output image
    output_image_pil = Image.fromarray(output_image.permute(1, 2, 0).numpy())

    output_image_pil.save(f"output_of_0_.jpg")

    # Release the camera and close all windows
    camera.stop()
    print('done')
