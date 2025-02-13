import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Simulate data for this example:
samples = 1000
time_steps = 20

# Simulate total oxygen consumption (in L/min) and total bed count for each time step in the hospital
oxygen_consumption_data = np.random.uniform(1000.0, 5000.0, (samples, time_steps, 1))  # Total hospital oxygen consumption
bed_count_data = np.random.randint(100, 500, (samples, time_steps, 1))  # Total bed count in the hospital

# Combine both features (total oxygen consumption and bed count) into one input array
X = np.concatenate([oxygen_consumption_data, bed_count_data], axis=-1)

# Simulate total oxygen consumption labels for prediction (next time step)
y = np.random.uniform(1500.0, 6000.0, samples)  # Total hospital oxygen consumption at next time step

# Normalize the data
scaler = StandardScaler()
X = scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Build the RNN Model
model = Sequential()
model.add(SimpleRNN(units=50, activation='relu', input_shape=(time_steps, 2)))
model.add(Dense(1))  # Output layer (predicted total oxygen consumption)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Predict the next step in total oxygen consumption for the hospital
predicted_consumption = model.predict(X_test)

# Example of a prediction output:
print(predicted_consumption)
