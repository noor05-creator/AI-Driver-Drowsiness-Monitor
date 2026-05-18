"""
analytics.py

Generates performance charts from training history
and session logs. Saves figures to /assets/.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


HISTORY_PATH = os.path.join("logs", "training_history.csv")
CURVES_PATH = os.path.join("assets", "training_curves.png")


def plot_training_curves():
    """
    Plot training vs validation accuracy and loss over epochs.

    Reads training_history.csv, creates a 2-subplot figure,
    and saves it to /assets/training_curves.png at 150 DPI.
    """
    os.makedirs("assets", exist_ok=True)

    df = pd.read_csv(HISTORY_PATH)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Accuracy subplot
    ax1.plot(df.index, df["accuracy"], label="Train Accuracy")
    ax1.plot(df.index, df["val_accuracy"], label="Val Accuracy")
    ax1.set_title("Training vs Validation Accuracy")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()

    # Loss subplot
    ax2.plot(df.index, df["loss"], label="Train Loss")
    ax2.plot(df.index, df["val_loss"], label="Val Loss")
    ax2.set_title("Training vs Validation Loss")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()

    fig.suptitle("CNN Eye State Classifier — Training Curves")
    plt.tight_layout()
    plt.savefig(CURVES_PATH, dpi=150)
    plt.close()
    print(f"Training curves saved to {CURVES_PATH}")


if __name__ == "__main__":
    plot_training_curves()
