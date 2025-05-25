import cv2

# Load image
image = cv2.imread("/sdcard/xvx.jpg")

# Convert to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define red color range (two ranges for full red hue spectrum)
lower_red1 = (0, 100, 100)
upper_red1 = (10, 255, 255)
lower_red2 = (160, 100, 100)
upper_red2 = (180, 255, 255)

# Create masks for red
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# Inpaint to remove red scribbles
cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

# Save output
cv2.imwrite("output.jpg", cleaned)