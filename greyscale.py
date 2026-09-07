import cv2
import matplotlib.pyplot as plt

# Load original image
img = cv2.imread("image.jpg")

# Convert BGR → RGB for displaying correctly with matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(f"size:{gray.shape}")

# Show both
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")

plt.show()

cv2.imwrite("test_image_grayscale.jpg", gray)