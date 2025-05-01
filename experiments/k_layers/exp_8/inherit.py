# Parent class
class AlgorithmBase:
    def __init__(self, data):
        self.data = data

    def preprocess(self):
        print("Preprocessing the data...")
        # common code here
        self.data = sorted(self.data)  # example

    def postprocess(self, result):
        print("Postprocessing the result...")
        return result * 2  # example

# Child class 1
class AlgorithmA(AlgorithmBase):
    def run(self):
        self.preprocess()
        print("Running Algorithm A")
        result = sum(self.data)
        return self.postprocess(result)

# Child class 2
class AlgorithmB(AlgorithmBase):
    def run(self):
        self.preprocess()
        print("Running Algorithm B")
        result = max(self.data)
        return self.postprocess(result)

# Example usage
data = [5, 1, 9, 3]

algo_a = AlgorithmA(data)
output_a = algo_a.run()
print(f"Result of Algorithm A: {output_a}")

algo_b = AlgorithmB(data)
output_b = algo_b.run()
print(f"Result of Algorithm B: {output_b}")
