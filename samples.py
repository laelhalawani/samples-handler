import random
import json


class Samples:
    """
    A class representing a set of input-output samples for a machine learning model.

    Parameters:
    samples_list_or_path (list or str): A list of samples or a path to a JSON file containing the samples.
    name (str): Arbitrary name for the set of samples, e.g. "training", "evaluation", "test".
    sample_input_key (str): The key in each sample dictionary that corresponds to the input data.
    sample_output_key (str): The key in each sample dictionary that corresponds to the output data.
    check_samples (bool): Whether to check the validity of the samples upon initialization.

    Methods:
    __len__(): Returns the number of samples in the set.
    __iter__(): Returns an iterator over the samples.
    __next__(): Returns the next sample in the iterator.
    __str__(): Returns a string representation of the Samples object.
    load_samples(samples_json_file): Loads samples from a JSON file.
    check_samples(): Checks the validity of the samples.
    get_all_samples(): Returns all samples in the set.
    shuffle(times=1): Shuffles the samples a specified number of times.
    split_samples_by_proportion(proportions_list=[0.7, 0.2, 0.1], names_list=["train", "eval", "test"], shuffle=1): Splits the samples into multiple sets by proportion.
    count(): Returns the number of samples in the set.
    """
class Samples:
    def __init__(self, samples_list_or_path, name="", sample_input_key="input", sample_output_key="target", validate_samples_len=False):
        """
        Initializes a Samples object.

        Args:
            samples_list_or_path (list or str): A list of samples or a path to a file containing samples.
            name (str, optional): A name for the Samples object. Defaults to "".
            sample_input_key (str, optional): The key for the input data in each sample. Defaults to "input".
            sample_output_key (str, optional): The key for the target data in each sample. Defaults to "target".
            valdiate_samples_len (bool, optional): Whether to check the the samples have equal len durng validity check of the samples. Defaults to False.
        """
        self.index = 0
        self.name = name
        self._input_key = sample_input_key
        self._target_key = sample_output_key
        if type(samples_list_or_path) == str:
            self.all_samples = self.load_samples(samples_list_or_path)
        else:
            self.all_samples = samples_list_or_path
        self.total_samples = len(self.all_samples)
        self.training_samples = None
        self.evaluation_samples = None
        self.current_training_id = None
        self.current_evaluation_id = None
        print(f"Created Samples object with {len(self.all_samples)} {name} samples")
        self.validate_samples(validate_samples_len)

    def __len__(self):
        return len(self.all_samples)
    def __iter__(self):
        return self

    def __next__(self):
        # The __next__ method returns the next value from the iterator
        if self.index < len(self.all_samples):
            result = self.all_samples[self.index]
            self.index += 1
            return result
        else:
            # Once all items are returned, the __next__ method raises a StopIteration exception
            raise StopIteration
    def __str__(self):
        return f'Samples( name: {self.name} | size: {len(self)})'
    
    def load_samples(self, samples_json_file:str) -> list:
        """
        Load samples from a JSON file.

        Args:
            samples_json_file (str): The path to the JSON file containing the samples.

        Returns:
            list: A list of samples loaded from the JSON file.
        """
        print(f"Loading samples from {samples_json_file}")
        with open(samples_json_file, 'r') as f:
            samples = json.load(f)
        return samples

    def validate_samples(self, padded=True):
        """
        Check that all samples have the same length and contain both input and target data.

        Raises:
            KeyError: If a sample is missing either "input" or "target" data.
            ValueError: If the length of the input and target data in a sample do not match.
        """
        sample_len = None
        for sample in self.all_samples:
            if not "input" in sample.keys() or not "target" in sample.keys():
                print(sample)
                raise KeyError("Missing input or target in sample")
            elif padded:
                input_len = len(sample["input"])
                output_len = len(sample["target"])
                if sample_len is None:
                    sample_len = input_len
                elif sample_len != input_len or sample_len != output_len or input_len != output_len:
                    raise ValueError(f"Sample length mismatch between input and target: {sample_len} vs. {input_len} vs. {output_len}")
                print(f"All samples have the same length: {sample_len}")
   
    def get_all_samples(self):
        """
        Returns all samples in the dataset.

        Returns:
            list: A list of all samples in the dataset.
        """
        return self.all_samples

    def shuffle(self, times=1):
        """
        Shuffle the list of samples in the object a specified number of times.

        Args:
            times (int): The number of times to shuffle the list of samples. Defaults to 1.

        Returns:
            None
        """
        for _ in range(times):
            random.shuffle(self.all_samples)
        print(f"Shuffled samples {times} time(s)")
    
    def split_samples_by_proportion(self, proportions_list=[0.7, 0.2, 0.1], names_list=["train", "eval", "test"], shuffle = 1):
        """
        Splits the samples into multiple subsets based on the given proportions and returns a list of Samples objects.

        Args:
            proportions_list (list of float, optional): A list of proportions for each subset. Defaults to [0.7, 0.2, 0.1].
            names_list (list of str, optional): A list of names for each subset. Defaults to ["train", "eval", "test"].
            shuffle (int, optional): A flag to shuffle the samples before splitting. Defaults to 1.

        Returns:
            list of Samples: A list of Samples objects, each containing a subset of the original samples.
        """
        #normalize list
        proportions_sum = sum(proportions_list)
        proportions_list = [p / proportions_sum for p in proportions_list]
        split_sizes = [int(p * self.total_samples) for p in proportions_list]
        #shuffle
        self.shuffle(shuffle)
        split_samples = []
        split_idx = 0
        for size in split_sizes:
            if size == 0:
                raise ValueError(f"Split size is 0, adjust proportions: {proportions_list} or use largert sample set, current size at {self.total_samples}")
            split_samples.append(self.all_samples[split_idx:split_idx+size])
            split_idx += size
        samples = []
        for i in range(len(split_samples)):
            if i < len(names_list):
                name = names_list[i]
            else:
                name = f"{i}"
            s = Samples(split_samples[i], name=name, sample_input_key=self._input_key, sample_output_key=self._target_key, validate_samples=False)
            samples.append(s)
        return samples
    

