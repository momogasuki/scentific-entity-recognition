import numpy as np

def conll2conll(data_file, dest_file):
    max_len = 200
    with open(data_file, 'rt', encoding='utf-8') as f:
        with open(dest_file, 'wt', encoding='utf-8') as w:
            count = 0
            for idx, line in enumerate(f.read().split('\n\n')):
                if not line:
                    break
                num = 0
                for i, item in enumerate(line.split('\n')):
                    try:
                        char,_,_, tag = item.split('\t')
                    except:
                        if count == 0:
                            print("The conll file is probably using spaces to separate tokens and ner tags. Trying to parse using spaces.")
                            count += 1
                        char,_,_, tag = item.split(' ')
                    if char == "." and i>=3 and i<(len(line.split('\n'))-1) and tag == 'O':
                        prev_sen = ''
                        for prev in line.split('\n')[i-2:i+1]:
                            c,_,_,_ = prev.split(' ')
                            prev_sen = prev_sen+c
                        if prev_sen != 'etal.':
                            num = 0
                            w.write(char+" "+tag+"\n\n")
                        else:
                            w.write(char+" "+tag+"\n")
                            num +=1
                    else:
                        w.write(char+" "+tag+"\n")
                        num+=1
                w.write("\n")
    return



if __name__ == "__main__":
    data_file = "../data/new_train_origin.conll"
    dest_file = "../data/new_train_post.conll"
    conll2conll(data_file, dest_file)