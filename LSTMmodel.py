import torch
import torch.nn as nn

class CharLSTM(nn.Module):
    def __init__(self, vocab_size=28, embedding_dim=64, hidden_dim=256, num_layers = 2, dropout_rate=0.5):
        super(CharLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers,batch_first=True,dropout=dropout_rate)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell)= self.lstm(embedded)
        lstm_out = self.dropout(lstm_out)
        output = self.fc(lstm_out)
        return output
