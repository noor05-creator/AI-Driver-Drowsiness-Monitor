import os
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten,
    Dense, Dropout, BatchNormalization
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam


DATA_DIR = "data"
MODEL_PATH = "model/drowsiness_cnn.h5"
HISTORY_PATH = "logs/training_history.csv"
IMG_SIZE = (24, 24)
BATCH_SIZE = 32
EPOCHS = 20


def build_model():
    """
    Build and compile the CNN model for eye state classification.

    The architecture uses two convolutional blocks followed by
    fully connected layers with dropout for regularization.

    Returns:
        tensorflow.keras.Model: Compiled CNN model ready for training.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(24, 24, 1)),
        MaxPooling2D((2, 2)),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model


def create_data_generators():
    """
    Create training and validation data generators with augmentation.

    Applies rescaling, rotation, and horizontal flip augmentation
    to the training data. Uses 20% of data for validation.

    Returns:
        tuple: (train_generator, val_generator) ImageDataGenerator objects.
    """
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2,
        rotation_range=10,
        horizontal_flip=True
    )

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )

    return train_generator, val_generator


def save_training_history(history):
    """
    Save the training history to a CSV file using Pandas.

    Args:
        history: Keras History object returned by model.fit().

    Returns:
        None
    """
    os.makedirs("logs", exist_ok=True)
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(HISTORY_PATH, index=False)
    print(f"Training history saved to {HISTORY_PATH}")


def plot_training_curves(history):
    """
    Plot and save training accuracy and loss curves using Matplotlib.

    Generates a figure with two subplots showing accuracy and loss
    over epochs for both training and validation sets.

    Args:
        history: Keras History object returned by model.fit().

    Returns:
        None
    """
    os.makedirs("assets", exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("CNN Training Performance", fontsize=14)

    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(
        history.history['val_accuracy'], label='Val Accuracy'
    )
    axes[0].set_title("Accuracy over Epochs")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()

    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Val Loss')
    axes[1].set_title("Loss over Epochs")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("assets/training_curves.png", dpi=150)
    plt.show()
    print("Training curves saved to assets/training_curves.png")


def train():
    """
    Run the full CNN training pipeline.

    Creates data generators, builds the model, trains it,
    saves the model and history, and plots training curves.

    Returns:
        None
    """
    print("Creating data generators...")
    train_gen, val_gen = create_data_generators()

    print("Building model...")
    model = build_model()
    model.summary()

    print(f"Training for {EPOCHS} epochs...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS
    )

    os.makedirs("model", exist_ok=True)
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print(f"Final training accuracy:   {final_train_acc:.4f}")
    print(f"Final validation accuracy: {final_val_acc:.4f}")

    save_training_history(history)
    plot_training_curves(history)


if __name__ == "__main__":
    train()