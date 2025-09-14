import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

class Matrix(NDArrayOperatorsMixin):
    def __init__(self, data):
        self._data = np.array(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = np.array(new_data)

    @property
    def shape(self):
        return self._data.shape

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self._data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        arrays = [x._data if isinstance(x, Matrix) else x for x in inputs]
        result = getattr(ufunc, method)(*arrays, **kwargs)
        if isinstance(result, tuple):
            return tuple(Matrix(x) if isinstance(x, np.ndarray) else x for x in result)
        elif isinstance(result, np.ndarray):
            return Matrix(result)
        else:
            return result

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape[1] != other.shape[0]:
            raise ValueError("Shapes not aligned for matrix multiplication")
        return Matrix(self._data @ other._data)

    def to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def to_string(self):
        return self.__str__()

def main():
    np.random.seed(0)

    A = Matrix(np.random.randint(1, 10, (10, 10)).tolist())
    B = Matrix(np.random.randint(1, 10, (10, 10)).tolist())

    (A + B).to_file("artifacts/task2/matrix+.txt")
    (A * B).to_file("artifacts/task2/matrix*.txt")
    (A @ B).to_file("artifacts/task2/matrix@.txt")

if __name__ == "__main__":
    main()
