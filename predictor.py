import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

class AISoiCauLSTM:
    def __init__(self, window_size=10, epochs=20, batch_size=8):
        self.window_size = window_size
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = self._build_model()
        self.trained = False

    def _build_model(self):
        model = Sequential()
        model.add(LSTM(50, input_shape=(self.window_size, 1), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))  # output 0 hoặc 1
        model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        return model

    def _create_features(self, data):
        X, y = [], []
        for i in range(self.window_size, len(data)):
            X.append(data[i - self.window_size:i])
            y.append(data[i])
        X = np.array(X)
        y = np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))  # reshape cho LSTM input
        return X, y

    def train(self, data):
        X, y = self._create_features(data)
        if len(X) == 0:
            raise ValueError("Không đủ dữ liệu để huấn luyện.")
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        self.trained = True

    def predict(self, data):
        if not self.trained:
            raise ValueError("Chưa huấn luyện.")
        if len(data) < self.window_size:
            raise ValueError("Không đủ dữ liệu.")
        last_window = np.array(data[-self.window_size:]).reshape(1, self.window_size, 1)
        prob = self.model.predict(last_window, verbose=0)[0][0]
        return 1 if prob >= 0.5 else 0
