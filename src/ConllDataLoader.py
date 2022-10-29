from torch.utils.data import Dataset

class conll_dataset(Dataset):
    def __init__(self, data_file):
        self.data, self.id2tag, self.tag2id = self.load_data(data_file)
    
    def load_data(self, data_file):
        Data = {'tokens': [],
                'ner_tags': [], 
                'labels': []}
        categories = set()
        with open(data_file, 'rt', encoding='utf-8') as f:
            count = 0
            for idx, line in enumerate(f.read().split('\n\n')):#for idx, line in enumerate(re.split(r'\n\t?\n',f.read())):
                if not line:
                    break
                tokens, ner_tags, labels = [], [], []
                for i, item in enumerate(line.split('\n')):
                    try:
                        char, tag = item.split('\t')
                    except:
                        if count == 0:
                            print("The conll file is probably using spaces to separate tokens and ner tags. Trying to parse using spaces.")
                            count += 1
                        char, tag = item.split(' ')
                    tokens.append(char)
                    ner_tags.append(tag)
                    #Entity extraction
                    if tag.startswith('B'):
                        labels.append([i, i, char, tag[2:]]) # Remove the B- or I-
                        categories.add(tag[2:])
                    elif tag.startswith('I'):
                        labels[-1][1] = i
                        labels[-1][2] += " "+char
                
                # # hacky
                # tokens = tokens[0:200]  
                # ner_tags = ner_tags[0:200]
                # labels = labels[0:200]
                
                Data['tokens'].append(tokens),
                Data['ner_tags'].append(ner_tags), 
                Data['labels'].append(labels)
        id2tag = {0:'O'}
        for c in list(sorted(categories)):
            id2tag[len(id2tag)] = f"B-{c}"
            id2tag[len(id2tag)] = f"I-{c}"
        tag2id = {v: k for k, v in id2tag.items()}
        for i in range(len(Data['ner_tags'])):
            for j in range(len(Data['ner_tags'][i])):
                Data['ner_tags'][i][j] = tag2id[Data['ner_tags'][i][j]]

        return Data, id2tag, tag2id

    def __len__(self):
        return len(self.data['tokens'])

    def __getitem__(self, idx):
        if idx == 'tokens':
            return self.data['tokens']
        elif idx == 'ner_tags':
            return self.data['ner_tags']
        elif idx == 'labels':
            return self.data['labels']
        else:
            return {'tokens':self.data['tokens'][idx], 
                'ner_tags':self.data['ner_tags'][idx],
                'labels':self.data['labels'][idx]}

if __name__ == "__main__":
    train_data = conll_dataset('train_post.conll')
    # with open('bert.txt', encoding='utf-8') as single:
    #     single=single.readlines()
    # print(single[4])
    # print(train_data[0]['sentence']+'\n')
    print(train_data[0:4])
    print(train_data.id2tag)