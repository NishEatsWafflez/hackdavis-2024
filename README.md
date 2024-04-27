# HackDavis 2024

Mission: Reduce car related injuries and deaths

## Parts of the whole system

### Lane Detection
Use a forward facing camera and OpenCV to recognize lanes and alert the driver if they do not stay within their lane.

### Driver Alertness Detection
Use a driver facing camera and OpenCV to detect if the driver is awake and paying attention to the road

### Blind Spot Detection
Use PyTorch and Intel Developer Cloud Notebook to detect pedestrians walking infront and next to the car and alert the driver if they get too close

### Proximity Alert
Use an Arduino and an ultrasonic distance sensor to alert the driver if they are too close to anything, including another car 

## Using Intel Developer Cloud for our PyTorch Model for Blind Stop Detection

![2024-04-27_14-38](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/04ad8614-f082-4455-9859-1f5221e16931)

![2024-04-27_15-19](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/185f2b9e-9423-44be-8b31-d537f304a16d)

![2024-04-27_15-23](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/a878533e-4dcf-426a-9683-86fece80e0d9)

## OpenCV Lane Detection

### Original Image
![lane-image](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/3457eaf7-1a5d-4db4-ac5f-d8cf5790430c)

### Black and White
![lane-image2](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/c0649056-c728-4da0-8a30-7acca806ef22)

### Canny Processing
![lane-image3](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/21a086e3-e459-4e64-8d68-96e1b0ea7f42)

### Applying a crop to area of interest
![lane-image4](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/02485c8c-fe6a-4ef2-b82b-07bb57c6df0f)

### Final by averaging out differences
![lane-image5](https://github.com/JakeRoggenbuck/hackdavis-2024/assets/35516367/cd855467-ebd7-48e9-b189-9b789f33adca)

