
import numpy as np
import preprocessing


benign_code_samples = 0 
malicious_code_samples = 0

def load_codes(benign_samples, malicious_samples):
    examples = []
    labels = []

    sample_count = 0
    with open('data/benign_codes.bin', 'rb') as f:
        while sample_count < benign_samples:
            line = f.readline()
            if not line: break
            line = byte_to_int8_conversion(line)
            if len(line) != 160000:
                continue
            examples.append(line)
            labels.append([1, 0])
            sample_count += 1

    sample_count = 0
    with open('data/malicious_codes.bin', 'rb') as f:
        while sample_count < malicious_samples:
            line = f.readline()
            if not line: break
            line = byte_to_int8_conversion(line)
            if len(line) != 160000:
                continue
            examples.append(line)
            labels.append([0, 1])
            sample_count += 1

    return examples, labels


def byte_to_int8_conversion(bin):
    bin = bin.replace(b' ', b'')
    res = []
    for n in bin[:-1]:
        if int(n) & 1:
           res.append(1)
        else:
           res.append(0)
    return np.array(res, dtype=np.int8)


def get_shaped_batch_input(flatten_batch_input, labels, start_index, end_index):
    target_batch_input = flatten_batch_input[start_index:end_index]
    shaped_batch_input = np.zeros(shape=[len(target_batch_input), 8, 20000, 1])
    shape = shaped_batch_input.shape
    for b in range(shape[0]):
        string_input = target_batch_input[b]
        for w in range(shape[2]):
            for h in range(shape[1]):
                shaped_batch_input[b][h][w][0] = string_input[w * shape[1] + h]
    return [shaped_batch_input, labels[start_index:end_index]]


def load_data(benign_samples, malicious_samples):
    examples, labels = load_codes(benign_samples, malicious_samples)
    x = np.array(examples, dtype=np.int8)
    y = np.array(labels, dtype=np.int8)
    print("x_char_seq_ind=" + str(x.shape))
    print("y shape=" + str(y.shape))
    return [x, y]


def batch_iter(x, y, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data_size = len(x)
    num_batches_per_epoch = int(data_size/batch_size) + 1
    for epoch in range(num_epochs):
        print("In epoch >> " + str(epoch + 1))
        print("num batches per epoch is: " + str(num_batches_per_epoch))
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            x_shuffled = x[shuffle_indices]
            y_shuffled = y[shuffle_indices]
        else:
            x_shuffled = x
            y_shuffled = y
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            x_batch, y_batch = get_shaped_batch_input(x_shuffled, y_shuffled, start_index, end_index)
            batch = list(zip(x_batch, y_batch))
            yield batch

