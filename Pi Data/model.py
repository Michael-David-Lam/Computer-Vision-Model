import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
# from keras.optimizers import Adam
from tensorflow.keras.optimizers.legacy import Adam # for mac only
from keras.callbacks import ModelCheckpoint, Callback
from keras.layers import Input, Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from utils import INPUT_SHAPE, batch_generator
import os

# ----------------------
# Configuration values
# ----------------------
data_dir = 'data' # directory where our training data is relative to CWD
test_size = 0.3 # use 70% of our data for training
# keep_prob = 0.5
nb_epoch = 10 # number of epochs
samples_per_epoch = 20000
batch_size = 40
bin_size=20 # for stratifying y values
save_best_only = True # whether to save the best trained model (based on validation loss) in all epochs or all of them
learning_rate = 0.00001

# for debugging, allows for reproducible (deterministic) results
np.random.seed(0)

def load_data():
    data_df = pd.read_csv(os.path.join(os.getcwd(), data_dir, './driving_log.csv'),
                          names=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed'])

    # The 3 camera images will be the input to our model (the X values)
    X = data_df[['center', 'left', 'right']].values
    # The steering wheel value will be output (the y values)
    y = data_df['steering'].values

    # Downsampling 0 steering wheel values because we have a lot of them
    # Convert to Pandas DataFrame for easier manipulation
    data = pd.DataFrame({'X': list(X), 'y': y})

    # Separate zero and non-zero steering angles
    zero_steering = data[data['y'] == 0]  # Rows where steering angle is 0
    non_zero_steering = data[data['y'] != 0]  # Rows where steering angle is non-zero

    zero_downsampled = zero_steering.sample(frac=0.25, random_state=42)  # Adjust fraction as needed

    # Combine downsampled zeros with non-zero steering angles
    balanced_data = pd.concat([zero_downsampled, non_zero_steering])

    # Shuffle the dataset
    balanced_data = balanced_data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Extract X and y after balancing
    X_balanced = np.array(list(balanced_data['X']))
    y_balanced = balanced_data['y'].values

    # Define bins for stratification
    bins = np.linspace(min(y_balanced), max(y_balanced), bin_size)

    # Digitize y values into bins for stratified splitting
    y_binned = np.digitize(y_balanced, bins)

    # Split into training and validation sets with stratification
    x_train, x_valid, y_train, y_valid = train_test_split(
        X_balanced, y_balanced, test_size=test_size, random_state=42, stratify=y_binned
    )

    # Plot distribution of steering angles
    plt.figure(figsize=(8, 6))
    plt.hist(y_train, alpha=0.7, bins=bin_size, color='green', edgecolor='black')
    plt.title('Distribution of Steering Angles After Balancing', fontsize=16)
    plt.xlabel('Steering Angle', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)
    plt.show()

    return x_train, x_valid, y_train, y_valid

# Plot the learning curve after each epoch
class LearningCurvePlotter(Callback):
    def __init__(self):
        super().__init__()
        self.training_loss = []
        self.validation_loss = []

    def on_epoch_end(self, epoch, logs=None):
        # Append current epoch's losses
        self.training_loss.append(logs['loss'])
        self.validation_loss.append(logs['val_loss'])

        # Clear current plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(self.training_loss) + 1), self.training_loss, label='Training Loss')
        plt.plot(range(1, len(self.validation_loss) + 1), self.validation_loss, label='Validation Loss')
        plt.title('Learning Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.pause(0.01)  # Pause to update the plot
        plt.show()

def build_model():
    model = Sequential()
    # Add an explicit Input layer
    model.add(Input(shape=INPUT_SHAPE))
    # The lambda function shifts the input pixel range that is [0, 255] to [-1, 1] for better training
    model.add(Lambda(lambda x: x / 127.5 - 1.0))
    model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Dropout(rate=0.5)) # Drops 50% of the units
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1))
    model.summary()

    return model

def train_model(model, x_train, x_valid, y_train, y_valid):
    plotter = LearningCurvePlotter()

    # Checkpoint to save the best model
    checkpoint = ModelCheckpoint(
        'model-{epoch:03d}.h5',
        monitor='val_loss',
        verbose=0,
        save_best_only=save_best_only,
        save_weights_only=False,
        mode='auto'
    )

    # Using Mean Squared Error as the loss function to minimize the average squared differences between predicted and
    # actual steering angle values
    model.compile(
        loss='mean_squared_error',
        optimizer=Adam(learning_rate=learning_rate)
    )

    # Fit the model using batch generators
    history = model.fit(
        batch_generator(data_dir, x_train, y_train, batch_size, True),
        steps_per_epoch=samples_per_epoch,
        epochs=nb_epoch,
        initial_epoch=0,
        validation_data=batch_generator(data_dir, x_valid, y_valid, batch_size, False),
        validation_steps = int(np.ceil(len(x_valid) / batch_size)),
        callbacks=[checkpoint, plotter],
        verbose=1
    )


#%%

# main function
if __name__ == "__main__":
    # Load our data
    x_train, x_valid, y_train, y_valid = load_data()

    # Build our model
    model = build_model()

    # Train the model on data, and save each model after every epoch
    train_model(model, x_train, x_valid, y_train, y_valid)

