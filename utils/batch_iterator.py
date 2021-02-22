class BatchIterator:
    def __init__(self, X, y, batch_size = 128):
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.batch_idx = 0
        self.ln = len(X)
    
    def __iter__(self):
        return self
    
    def __len__(self):
        return int(self.ln / self.batch_size) + 1
    
    def __next__(self):
        start = self.batch_idx * self.batch_size
        if start >= self.ln:
            raise StopIteration
        end = (self.batch_idx + 1) * self.batch_size
        end = min(end, self.ln)
        self.batch_idx += 1
        return self.X[start:end], self.y[start:end]