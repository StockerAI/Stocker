import yfinance as yf
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

batch_size = 1

# Load the data for the S&P 500
stock_data = yf.download("AAPL", start="2010-01-01", end="2022-02-25")

# Normalize the data
stock_data["Adj Close"] = stock_data["Adj Close"] / stock_data["Adj Close"].max()

# Split the data into training and testing sets
train_size = int(len(stock_data) * 0.8)
train_data = stock_data.iloc[:train_size]["Adj Close"].values
test_data = stock_data.iloc[train_size:]["Adj Close"].values

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, input):
        lstm_out, _ = self.lstm(input.view(len(input), 1, -1))
        out = self.fc(lstm_out.view(len(input), -1))
        return out[-1]

# Define the model
model = LSTM(input_size=1, hidden_size=64, output_size=1)

# Define the loss function and optimizer
criterion = nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 100
train_losses = []
for epoch in range(num_epochs):
    train_loss = 0.0
    hidden = model.init_hidden(batch_size)
    for i in range(len(train_data)-1):
        # Prepare the input and target tensors
        input_tensor = torch.Tensor(train_data[i:i+1])
        target_tensor = torch.Tensor(train_data[i+1:i+2])

        # Forward pass
        output = model(input_tensor)

        # Calculate the loss and do the backward pass
        loss = criterion(output, target_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    train_losses.append(train_loss)

    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}/{num_epochs}, Training Loss: {train_loss:.4f}")

# Evaluate the model on the test data
model.eval()
with torch.no_grad():
    test_inputs = torch.Tensor(test_data[:-1]).squeeze()
    test_outputs = []
    hidden = model.init_hidden(batch_size)
    with torch.no_grad():
        for i in range(len(test_data) - 1):
            input_tensor = torch.Tensor([[test_data[i]]])
            output = model(input_tensor)
            test_outputs.append(output.item())
    test_outputs = [test_data[0]] + test_outputs

# Plot the results
plt.plot(stock_data["Adj Close"].values, label="Actual")
plt.plot(range(train_size, len(stock_data)), test_outputs, label="Predicted")
plt.legend()
plt.show()

