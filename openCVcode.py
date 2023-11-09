# Post color to Airtable
import numpy as np
import requests


# ----------- Find primary color of image ----------- #

COLOR = "" # global variable for image color
tempUnits = ""


# Finding average color of image
cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
height, width, _ = np.shape(cv2_image)
avg_color_per_row = np.average(cv2_image, axis=0)
avg_colors = np.average(avg_color_per_row, axis=0)
print(f'avg_colors: {avg_colors}')
int_averages = np.array(avg_colors, dtype=np.uint8)
print(f'int_averages: {int_averages}')

# Creating numpy arrays to compare BGR values to to identify color
int_averages = np.array([int_averages])
R_lowerrange = np.array([0,0,160])
R_upperrange = np.array([100,100,255])
G_lowerrange = np.array([0,180,0])
G_upperrange = np.array([100,255,100])
R_checklower = (int_averages >= R_lowerrange).all()
R_checkupper = (int_averages < R_upperrange).all()
G_checklower = (int_averages >= G_lowerrange).all()
G_checkupper = (int_averages < G_upperrange).all()

# Comparing image BGR values to thresholds
if (R_checklower == True) and (R_checkupper == True):
    COLOR = "red"
elif (G_checklower == True) and (G_checkupper == True):
    COLOR = "green"
else:
    COLOR = "Unknown"

print(COLOR)

# ----------- Post units to Airtable ----------- #

print("the color is: ", COLOR)
if COLOR == "green":
	tempUnits = "F"
elif COLOR == "red":
	tempUnits = "C"
else:
	tempUnits = "Unknown"

print("Temperature units are: ", tempUnits)

# Airtable setup
headers = {
    'Authorization': 'Bearer [API KEY]', # add API key
    'Content-Type': 'application/json',
}

# Posting to "Units" field of Airtable sheet
json_data = {
    'records': [
        {
            'id': 'recuPP1WjXBXAuIpB',
            'fields': {
                'Units': tempUnits,
            },
        },
    ],
}

try:
    response = requests.patch('https://api.airtable.com/v0/[BaseID]/Table%201', headers=headers, json=json_data) # add base ID
    print("Successful post")
except:
    print(response.status_code)
