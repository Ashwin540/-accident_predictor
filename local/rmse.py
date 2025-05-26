import matplotlib.pyplot as plt

# Replace these values with your actual RMSE results
locations = ['Location A', 'Location B', 'Location C', 'Location D', 'Location E']
rmse_knn = [4.5, 4.7, 4.4, 4.6, 4.5]   # KNN RMSE values
rmse_gbm = [3.2, 3.1, 3.0, 3.3, 3.1]   # GBM RMSE values

# Plotting the line graph
plt.figure(figsize=(10, 6))
plt.plot(locations, rmse_knn, marker='o', label='KNN', color='red')
plt.plot(locations, rmse_gbm, marker='o', label='GBM', color='blue')

# Adding labels and title
plt.title('RMSE Comparison: KNN vs GBM')
plt.xlabel('Test Locations')
plt.ylabel('RMSE Value')
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
