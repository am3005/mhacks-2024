import torch
from torch import nn
from torch.optim import Adam
from LSTMmodel import CharLSTM
from LSTMdataset import get_dataset, char_to_idx, idx_to_char

def train(model, num_epochs=1000, learning_rate=0.001):
    # Define the loss function and optimizer
    loss_fn = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    input_tensor, output_tensor = get_dataset()
    input_tensor, output_tensor = input_tensor.to(device), output_tensor.to(device)

    for epoch in range(num_epochs):
        model.train()
        output = model(input_tensor)
        output = output.permute(0, 2, 1)  # Ensure the output shape is correct
        loss = loss_fn(output, output_tensor)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
        optimizer.step()

        if epoch % 10 == 0:
            print(f'Epoch [{epoch}/{num_epochs}], Loss: {loss.item():.4f}')

    # Save the model after training
    torch.save(model.state_dict(), "char_level_model.pth")

# If this file is run directly, train the model
if __name__ == "__main__":
    vocab_size = len(char_to_idx)
    embedding_dim = 64
    hidden_dim = 256

    model = CharLSTM(vocab_size, embedding_dim, hidden_dim)
    train(model)  # Call the training function directly
