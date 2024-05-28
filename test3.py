import matplotlib.pyplot as plt

# Define data (example)
data = [15, 30, 25, 40]
labels = ["Red", "Green", "Blue", "Yellow"]

# Create the pie chart
plt.pie(data, labels=labels, autopct="%1.1f%%")
plt.title("Sunburst Pie Chart")
plt.show()
