# import re, os, random, tarfile, urllib
# from torchtext import data
from torch.utils.data import DataLoader, Dataset
#
# class TarDataset(data.Dataset):
#     @classmethod
#     def download_or_unzip(cls, root):
#         path = os.path.join(root, cls.dirname)
#         if not os.path.isdir(path):
#             tpath = os.path.join(root, cls.filename)
#             if not os.path.isfile(tpath):
#                 print('downloading')
#                 urllib.request.urlretrieve(cls.url, tpath)
#             with tarfile.open(tpath, 'r') as tfile:
#                 print('extracting')
#                 tfile.extractall(root)
#         return os.path.join(path, '')
#
# class MR(TarDataset):
#     url = 'https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz'
#     filename = 'rt-polaritydata.tar'
#     dirname = 'rt-polaritydata'
#
#     @staticmethod
#     def sort_key(ex):
#         return len(ex.text)
#
#     def __init__(self, text_field, label_field, path=None, examples=None, **kwargs):
#         """Create an MR dataset instance given a path and fields.
#         Arguments:
#             text_field: The field that will be used for text data.
#             label_field: The field that will be used for label data.
#             path: Path to the data file.
#             examples: The examples contain all the data.
#             Remaining keyword arguments: Passed to the constructor of
#                 data.Dataset.
#         """
#
#         def clean_str(string):
#             """
#             Tokenization/string cleaning for all datasets except for SST.
#             Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
#             """
#             string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
#             string = re.sub(r"\'s", " \'s", string)
#             string = re.sub(r"\'ve", " \'ve", string)
#             string = re.sub(r"n\'t", " n\'t", string)
#             string = re.sub(r"\'re", " \'re", string)
#             string = re.sub(r"\'d", " \'d", string)
#             string = re.sub(r"\'ll", " \'ll", string)
#             string = re.sub(r",", " , ", string)
#             string = re.sub(r"!", " ! ", string)
#             string = re.sub(r"\(", " \( ", string)
#             string = re.sub(r"\)", " \) ", string)
#             string = re.sub(r"\?", " \? ", string)
#             string = re.sub(r"\s{2,}", " ", string)
#             return string.strip()
#
#         text_field.preprocessing = data.Pipeline(clean_str)
#         fields = [('text', text_field), ('label', label_field)]
#
#         if examples is None:
#             path = self.dirname if path is None else path
#             examples = []
#             with open(os.path.join(path, 'rt-polarity.neg'), errors='ignore') as f:
#                 examples += [
#                     data.Example.fromlist([line, 'negative'], fields) for line in f]
#             with open(os.path.join(path, 'rt-polarity.pos'), errors='ignore') as f:
#                 examples += [
#                     data.Example.fromlist([line, 'positive'], fields) for line in f]
#         super(MR, self).__init__(examples, fields, **kwargs)
#
#     @classmethod
#     def splits(cls, text_field, label_field, dev_ratio=.1, shuffle=True, root='.', **kwargs):
#         """Create dataset objects for splits of the MR dataset.
#         Arguments:
#             text_field: The field that will be used for the sentence.
#             label_field: The field that will be used for label data.
#             dev_ratio: The ratio that will be used to get split validation dataset.
#             shuffle: Whether to shuffle the data before split.
#             root: The root directory that the dataset's zip archive will be
#                 expanded into; therefore the directory in whose trees
#                 subdirectory the data files will be stored.
#             train: The filename of the train data. Default: 'train.txt'.
#             Remaining keyword arguments: Passed to the splits method of
#                 Dataset.
#         """
#         path = cls.download_or_unzip(root)
#         examples = cls(text_field, label_field, path=path, **kwargs).examples
#         if shuffle: random.shuffle(examples)
#         dev_index = -1 * int(dev_ratio * len(examples))
#
#         return (cls(text_field, label_field, examples=examples[:dev_index]),
#                 cls(text_field, label_field, examples=examples[dev_index:]))
#
#
# def get_MR(text_field, label_field, batch_size, **kargs):
#     train_data, dev_data = MR.splits(text_field, label_field)
#     text_field.build_vocab(train_data, dev_data)
#     label_field.build_vocab(train_data, dev_data)
#     train_iter, dev_iter = data.Iterator.splits(
#         (train_data, dev_data),
#         batch_sizes=(batch_size, len(dev_data)),
#         **kargs)
#     return train_iter, dev_iter
#
# if __name__ == "__main__":
#     print("Loading data...")
#     text_field = data.Field(lower=True)
#     label_field = data.Field(sequential=False)
#     train_iter, dev_iter = get_MR(text_field, label_field,
#                                   device=-1, repeat=False,
#                                   batch_size=10)
#     print("Prepare data complete!")
#
#     for batch in train_iter:
#         feature, target = batch.text, batch.label
#         print(feature)
#         print(target)
#         break
#
# from sklearn.utils import shuffle
# def get_MR():
#     data = {}
#     x, y = [], []
#
#     with open("rt-polaritydata/rt-polarity.pos", "r", errors="ignore") as f:
#         for line in f:
#             if line[-1] == "\n":
#                 line = line[:-1]
#             x.append(line.split())
#             y.append(1)
#
#     with open("rt-polaritydata/rt-polarity.neg", "r", errors="ignore") as f:
#         for line in f:
#             if line[-1] == "\n":
#                 line = line[:-1]
#             x.append(line.split())
#             y.append(0)
#
#     x, y = shuffle(x, y)
#     val_idx = len(x) // 10 * 8
#     test_idx = len(x) // 10 * 9
#
#     data["train_x"], data["train_y"] = x[:val_idx], y[:val_idx]
#     data["val_x"], data["val_y"] = x[val_idx:test_idx], y[val_idx:test_idx]
#     data["test_x"], data["test_y"] = x[test_idx:], y[test_idx]
#
#     return data
#
# class MRSet(Dataset):
#     def __init__(self, data_x, data_y):
#         self.data_x = data_x
#         self.data_y = data_y
#
#     def __len__(self):
#         return len(self.data_x)
#
#     def __getitem__(self, idx):
#         return self.data_x[idx], self.data_y[idx]
#
# def get_loader(batch_size):
#     data = get_MR()
#     train_set = MRSet(data['train_x'], data['train_y'])
#     # print(train_set[0])
#     val_set = MRSet(data['val_x'], data['val_y'])
#     test_set = MRSet(data['test_x'], data['test_y'])
#     train_loader = DataLoader(dataset=train_set,
#                               shuffle=True,
#                               batch_size=batch_size)
#     val_loader = DataLoader(dataset=val_set,
#                             shuffle=True,
#                             batch_size=batch_size)
#     test_loader = DataLoader(dataset=test_set,
#                               shuffle=True,
#                              batch_size=batch_size)
#
#     return train_loader, val_loader, test_loader
#
#
# if __name__ == "__main__":
#
#     train, val, test = get_loader()
#     for step, (content, label) in enumerate(train):
#         print(content)
#         print(label)
#         break

import re, os, random, tarfile, urllib
from torchtext import data

class TarDataset(data.Dataset):
    @classmethod
    def download_or_unzip(cls, root):
        path = os.path.join(root, cls.dirname)
        if not os.path.isdir(path):
            tpath = os.path.join(root, cls.filename)
            if not os.path.isfile(tpath):
                print('downloading')
                urllib.request.urlretrieve(cls.url, tpath)
            with tarfile.open(tpath, 'r') as tfile:
                print('extracting')
                tfile.extractall(root)
        return os.path.join(path, '')

class MR(TarDataset):
    url = 'https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz'
    filename = 'rt-polaritydata.tar'
    dirname = 'rt-polaritydata'

    @staticmethod
    def sort_key(ex):
        return len(ex.text)

    def __init__(self, text_field, label_field, path=None, examples=None, **kwargs):
        """Create an MR dataset instance given a path and fields.
        Arguments:
            text_field: The field that will be used for text data.
            label_field: The field that will be used for label data.
            path: Path to the data file.
            examples: The examples contain all the data.
            Remaining keyword arguments: Passed to the constructor of
                data.Dataset.
        """

        def clean_str(string):
            """
            Tokenization/string cleaning for all datasets except for SST.
            Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
            """
            string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
            string = re.sub(r"\'s", " \'s", string)
            string = re.sub(r"\'ve", " \'ve", string)
            string = re.sub(r"n\'t", " n\'t", string)
            string = re.sub(r"\'re", " \'re", string)
            string = re.sub(r"\'d", " \'d", string)
            string = re.sub(r"\'ll", " \'ll", string)
            string = re.sub(r",", " , ", string)
            string = re.sub(r"!", " ! ", string)
            string = re.sub(r"\(", " \( ", string)
            string = re.sub(r"\)", " \) ", string)
            string = re.sub(r"\?", " \? ", string)
            string = re.sub(r"\s{2,}", " ", string)
            return string.strip()

        text_field.preprocessing = data.Pipeline(clean_str)
        fields = [('text', text_field), ('label', label_field)]

        if examples is None:
            path = self.dirname if path is None else path
            examples = []
            with open(os.path.join(path, 'rt-polarity.neg'), errors='ignore') as f:
                examples += [
                    data.Example.fromlist([line, 'negative'], fields) for line in f]
            with open(os.path.join(path, 'rt-polarity.pos'), errors='ignore') as f:
                examples += [
                    data.Example.fromlist([line, 'positive'], fields) for line in f]
        super(MR, self).__init__(examples, fields, **kwargs)

    @classmethod
    def splits(cls, text_field, label_field, dev_ratio=.1, shuffle=True, root='.', **kwargs):
        """Create dataset objects for splits of the MR dataset.
        Arguments:
            text_field: The field that will be used for the sentence.
            label_field: The field that will be used for label data.
            dev_ratio: The ratio that will be used to get split validation dataset.
            shuffle: Whether to shuffle the data before split.
            root: The root directory that the dataset's zip archive will be
                expanded into; therefore the directory in whose trees
                subdirectory the data files will be stored.
            train: The filename of the train data. Default: 'train.txt'.
            Remaining keyword arguments: Passed to the splits method of
                Dataset.
        """
        path = cls.download_or_unzip(root)
        examples = cls(text_field, label_field, path=path, **kwargs).examples
        if shuffle: random.shuffle(examples)
        dev_index = -1 * int(dev_ratio * len(examples))

        return (cls(text_field, label_field, examples=examples[:dev_index]),
                cls(text_field, label_field, examples=examples[dev_index:]))


def get_MR(text_field, label_field, batch_size, **kargs):
    train_data, dev_data = MR.splits(text_field, label_field)
    text_field.build_vocab(train_data, dev_data)
    label_field.build_vocab(train_data, dev_data)
    train_iter, dev_iter = data.Iterator.splits(
        (train_data, dev_data),
        batch_sizes=(batch_size, len(dev_data)),
        **kargs)
    return train_iter, dev_iter

if __name__ == "__main__":
    print("Loading data...")
    text_field = data.Field(lower=True)
    label_field = data.Field(sequential=False)
    train_iter, dev_iter = get_MR(text_field, label_field,
                                  device=-1, repeat=False,
                                  batch_size=10)
    print("Prepare data complete!")

    for batch in train_iter:
        feature, target = batch.text, batch.label
        print(feature)
        print(target)
        break