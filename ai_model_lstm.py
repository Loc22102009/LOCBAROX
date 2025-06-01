import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

class AISoiCauLSTM:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.model = None
        self.trained = False

    def _prepare_data(self, data):
        X, y = [], []
        for i in range(len(data) - self.window_size):
            X.append(data[i:i + self.window_size])
            y.append(data[i + self.window_size])
        X = np.array(X)
        y = np.array(y)
        return X[..., np.newaxis], y

    def train(self, data):
        X, y = self._prepare_data(data)
        self.model = Sequential([
            LSTM(32, input_shape=(self.window_size, 1)),
            Dense(1, activation='sigmoid')
        ])
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
        self.model.fit(X, y, epochs=50, verbose=0)
        self.trained = True

    def predict(self, data):
        if not self.trained or self.model is None:
            raise Exception("Model chưa được huấn luyện.")
        if len(data) < self.window_size:
            raise Exception(f"Cần ít nhất {self.window_size} phần tử để dự đoán.")
        input_data = np.array(data[-self.window_size:])[np.newaxis, ..., np.newaxis]
        pred = self.model.predict(input_data, verbose=0)[0][0]
        return 1 if pred >= 0.5 else 0
