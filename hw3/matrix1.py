import numpy as np

class Matrix:
    def __init__(self, data):
        if not data or len({len(row) for row in data}) != 1:
            raise ValueError("The matrix should be non-empty.")
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])

    def __add__(self, other):
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise ValueError("Addition is possible only for matrices of the same size.")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if (self.rows, self.cols) != (other.rows, other.cols):
            raise ValueError("Element-wise multiplication is possible only for matrices of the same size.")
        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns of the first matrix must match the number of rows of the second matrix for matrix multiplication.")
        res = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                s = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row.append(s)
            res.append(row)
        return Matrix(res)

    def to_string(self):
        return "\n".join(" ".join(map(str, row)) for row in self.data)

    def to_file(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.to_string())

def main():
    np.random.seed(0)

    A = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    B = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    (A + B).to_file('artifacts/task1/matrix+.txt')
    (A * B).to_file('artifacts/task1/matrix*.txt')
    (A @ B).to_file('artifacts/task1/matrix@.txt')

if __name__ == "__main__":
    main()