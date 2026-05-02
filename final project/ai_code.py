import numpy as np
# ==========================================
# 1. НЕЙРОСЕТЬ (Исправлена под регрессию)
# ==========================================
class DenseLayer:
    def __init__(self, units, activation='relu', input_dim=None):
        self.units = units
        self.activation = activation
        self.input_dim = input_dim
        self.weights = None
        self.biases = None

        self.input = None
        self.output = None

    def initialize(self, input_dim):
        self.input_dim = input_dim
        if self.activation == 'relu':
            limit = np.sqrt(2 / input_dim)
        else:
            limit = np.sqrt(6 / (input_dim + self.units))
        self.weights = np.random.uniform(-limit, limit, (input_dim, self.units))
        self.biases = np.zeros((1, self.units))

    def forward(self, X):
        self.input = X
        z = np.dot(self.input, self.weights) + self.biases
        if self.activation == "relu":
            self.output = np.maximum(0, z)
        elif self.activation == "sigmoid":
            self.output = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        elif self.activation == "linear":
            self.output = z
        elif self.activation == "softmax":
            z_safe = z - np.max(z, axis=-1, keepdims=True)
            e_z = np.exp(z_safe)
            self.output = e_z / np.sum(e_z, axis=-1, keepdims=True)
        return self.output

    def backward(self, grad_values, learning_rate):
        if self.activation == "relu":
            grad_activation = np.where(self.output > 0, 1, 0)
        elif self.activation == "linear":
            grad_activation = 1.0
        else:
            grad_activation = 1.0

        grad_inputs = grad_values * grad_activation
        self.grad_weights = np.dot(self.input.T, grad_inputs)
        self.grad_biases = np.sum(grad_inputs, axis=0, keepdims=True)
        prev_grad = np.dot(grad_inputs, self.weights.T)

        self.weights -= learning_rate * self.grad_weights
        self.biases -= learning_rate * self.grad_biases
        return prev_grad

class Sequential:
    def __init__(self):
        self.layers = []
        self.history = {'loss': [], 'val_loss': []}

    def add(self, layer):
        self.layers.append(layer)

    def compile(self, loss='mse'):
        if self.layers[0].weights is not None:
            raise RuntimeError("⚠️ Веса уже инициализированы/загружены! Вызов compile() их сотрёт.")
        self.loss_func = loss
        self.layers[0].initialize(self.layers[0].input_dim)
        cur_dim = self.layers[0].units
        for layer in self.layers[1:]:
            layer.initialize(cur_dim)
            cur_dim = layer.units

    def _calculate_loss(self, y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)

    def _loss_gradient(self, y_true, y_pred):
        n = len(y_true)
        return -2 * (y_true - y_pred) / n

    def predict(self, X):
        out = X
        for layer in self.layers:
            out = layer.forward(out)
        return out

    def fit(self, X, y, epochs=50, learning_rate=0.01, validation_split=0.1, verbose=1):
        split_idx = int(len(X) * (1 - validation_split))
        X_tr, X_val = X[:split_idx], X[split_idx:]
        y_tr, y_val = y[:split_idx], y[split_idx:]

        for epoch in range(epochs):
            y_pred = self.predict(X_tr)
            loss = self._calculate_loss(y_tr, y_pred)
            grad = self._loss_gradient(y_tr, y_pred)

            for layer in reversed(self.layers):
                grad = layer.backward(grad, learning_rate)

            val_pred = self.predict(X_val)
            val_loss = self._calculate_loss(y_val, val_pred)
            self.history['loss'].append(loss)
            self.history['val_loss'].append(val_loss)

            if verbose > 0 and (epoch % 10 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch}: loss = {loss:.4f}, val_loss = {val_loss:.4f}")

    def save(self, filepath, X_mean, X_std, y_mean, y_std):
        data = {
            'n_layers': len(self.layers),
            'X_mean': X_mean, 'X_std': X_std,
            'y_mean': y_mean, 'y_std': y_std
        }
        for i, layer in enumerate(self.layers):
            data[f'W_{i}'] = layer.weights
            data[f'b_{i}'] = layer.biases
            data[f'act_{i}'] = layer.activation
            data[f'units_{i}'] = layer.units

        np.savez_compressed(filepath, **data)
        print(f"💾 Веса и параметры нормализации сохранены в {filepath}")

    @classmethod
    def load(cls, filepath):
        data = np.load(filepath, allow_pickle=True)
        print(data.files)
        model = cls()

        for i in range(int(data['n_layers'])):
            layer = DenseLayer(
                units=int(data[f'units_{i}']),
                activation=str(data[f'act_{i}'])
            )
            layer.weights = data[f'W_{i}']
            layer.biases = data[f'b_{i}']
            layer.input_dim = layer.weights.shape[0]  # Восстанавливаем входную размерность
            model.add(layer)

        scaler = {
            'X_mean': data['X_mean'], 'X_std': data['X_std'],
            'y_mean': data['y_mean'], 'y_std': data['y_std']
        }
        print(f"📥 Модель успешно загружена из {filepath}")
        return model, scaler