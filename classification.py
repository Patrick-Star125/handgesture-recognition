import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import numpy as np



class Classification_Dataloader(Dataset):
    def __init__(self, hands_lines):
        super(Classification_Dataloader, self).__init__()
        self.hands_lines = hands_lines

    def __len__(self):
        return len(self.hands_lines)

    def __getitem__(self, index):
        hands_lines = self.hands_lines
        hand_steam = hands_lines[index][:-1]
        tmp_target = torch.tensor([int(hands_lines[index][-1])])

        tmp_hand = torch.tensor(hand_steam).reshape((10, 14, 2))

        return tmp_hand, tmp_target


def classification_collate(batch):
    '''此时batch为1'''
    hands = []
    # targets = []
    for hand, target in batch:
        hand = torch.split(hand, 1, dim=-1)
        hand = torch.stack((torch.squeeze(hand[0]), torch.squeeze(hand[1])), dim=0)
        hands.append(hand)
        targets = target
        # targets.append(target)

    hands = torch.stack(hands)
    # hands = torch.squeeze(hands.permute(0, 1, 3, 2))
    hands = torch.squeeze(hands)
    # targets = torch.stack(targets)
    return hands, targets


class Classification(nn.Module):
    def __init__(self):
        super(Classification, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv1d(10, 100, kernel_size=3, stride=1, padding=0),
                                   nn.BatchNorm1d(100),
                                   nn.ReLU(True))
        self.conv2 = nn.Sequential(nn.Conv1d(100, 100, kernel_size=3, stride=1, padding=0),
                                   nn.BatchNorm1d(100),
                                   nn.ReLU(True))
        self.conv3 = nn.Sequential(nn.Conv1d(100, 160, kernel_size=3, stride=1, padding=0),
                                   nn.BatchNorm1d(160),
                                   nn.ReLU(True))
        self.conv4 = nn.Sequential(nn.Conv1d(160, 160, kernel_size=3, stride=1, padding=0),
                                   nn.BatchNorm1d(160),
                                   nn.ReLU(True))
        self.avepooling = nn.AvgPool1d(2, stride=1)
        self.maxpooling = nn.MaxPool1d(5, stride=1)
        self.dropout = nn.Dropout(p=0.5)
        self.fc = nn.Sequential(nn.Linear(320, 5), nn.Softmax(dim=0))

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.maxpooling(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.avepooling(x)
        x = x.reshape(320)
        x = self.dropout(x)
        # x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

    def train_model(self, data, batch, learning_rate, num_epoches, save=True):
        '''训练模型并保存'''

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        dataset = Classification_Dataloader(data)
        train_dataset = DataLoader(dataset, batch_size=batch, shuffle=True, collate_fn=classification_collate)

        model = Classification().to(device)
        model.train(mode=True)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        total_step = len(train_dataset)
        for epoch in range(num_epoches):
            for i, hands in enumerate(train_dataset):
                hand, label = hands
                hand = hand.to(device)
                label = label.to(device)

                optimizer.zero_grad()
                outputs = model(hand)
                outputs = outputs.unsqueeze(dim=0)
                loss = criterion(outputs, label)

                loss.backward()
                optimizer.step()

                if (i + 1) % 50 == 0:
                    print('Epoch [{}/{}], Step [{}/{}], Loss:{:.4f}'.format(epoch + 1, num_epoches, i + 1, total_step,
                                                                            loss.item()))
                    print('outputs:{}'.format(outputs.tolist()))
                    if i+1 == 100:
                        b=1

        if save:
            # summary(model, (2, 5, 42))
            torch.save(model.state_dict(),
                       'num_{}_batch_{}_lr_{}_ep_{}.pth'.format(1, batch, learning_rate, num_epoches))

    def predict(self, hand, file):
        '''加载模型进行推理'''
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        hands = torch.tensor(hand).reshape((10, 14, 2))
        hands = torch.split(hands, 1, dim=-1)
        hands = torch.stack((torch.squeeze(hands[0]), torch.squeeze(hands[1])), dim=0)
        # hands = hands.permute(0, 2, 1)
        # hands = hands.reshape((1, 2, 5, 42))
        hands = hands.to(device)
        model = Classification().to(device)
        model.load_state_dict(torch.load(file,map_location='cpu'))
        model.eval()

        result = model(hands)

        return result



# # troch.nn.RNN(input_size,hidden_size,num_layers)
# rnn = nn.RNN(10, 20, 2)
# # input1 = (L,N,H) tensor containing input features where H =input_size and L represents a sequence length.
# input = torch.randn(5, 3, 10)
# # input2 = (S,N,H)  tensor containing the initial hidden state for each element in the batch. H=hidden_size Defaults to zero if not provided. where S=num_layers∗num_directions If the RNN is bidirectional, num_directions should be 2, else it should be 1.
# h0 = torch.randn(2, 3, 20)
# # output1 = (L,N,H) where H = num_directions * hidden_size
# # output2 = (S,N,H) tensor containing the next hidden state for each element in the batch
# output, hn = rnn(input, h0)
# a = 1