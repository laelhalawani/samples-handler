# Samples Class Documentation

- [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Initialize Samples Object](#initialize-samples-object)
  - [Load Samples](#load-samples)
  - [Shuffle Samples](#shuffle-samples)
  - [Split Samples](#split-samples) 
  - [Iterate Through Samples](#iterate-through-samples)
  - [Get Number of Samples](#get-number-of-samples)
- [API Reference](#api-reference)


## Introduction and Overview
The `Samples` class represents a set of input-output samples for a machine learning model. It is an iterable object providing methods to load samples from a JSON file, check the validity of the samples, shuffle the samples and split the samples into multiple subsets.

The object expects data following a format - a list of dictionaries, each with key `input` for input sequence and `output` for output sequence.
The output can be a string or a list of elements such as token ids or tokens. 
```JSON
[
    {
        "input":"iterable input sequence 1",
        "target":"iterable target squence 1", 
    },
]
```
or
```JSON
[
    {
        "input":[-999, -2, -1, 0],
        "target":[0, 0, 0, -1], 
    },
]
```

## Installation
To install the Samples hadnler, you can download the repository and open a command prompt in the extracted directory. Then, run the following command:
```python
pip install .
```
You can then import the class into your Python script
using 

```python
from samples_handler import Samples
```

## Samples Class Usage Guide
### Initialize a Samples Object
You can quickly initialize `Samples` object by providing a list of samples or a path to a JSON file containing the samples. 
```python
samples = Samples(samples_list_or_path='./samples.json')
```
You can also specify the keys for the input and target data in each sample, and if it's different than the desired for example `"input"` and `"output"`.
```python
samples = Samples(samples_list_or_path='./samples.json', name="my samples", sample_input_key="input", sample_output_key="target")
```
### Get All Samples
You can get all samples in the dataset using the `get_all_samples` method.
```python
samples = Samples('samples.json')
all_samples = samples.get_all_samples()
```

### Split the Samples by Proportion
You can split the samples into multiple subsets based on the given proportions using the `split_samples_by_proportion` method. This method returns a list of Samples objects, each containing a subset of the original samples. 
```python
samples = Samples('samples.json')
split_samples = samples.split_samples_by_proportion(proportions_list=[0.7, 0.2, 0.1], names_list=["train", "eval", "test"], shuffle=1)
```
you can also use python's sequence unpacking to assign each part to a new variable, just keep the number of variables equal to number of splits
```python
samples = Samples('samples.json')
train, evaluate, test = samples.split_samples_by_proportion(proportions_list=[0.7, 0.2, 0.1], names_list=["train", "eval", "test"], shuffle=1)
```
### Iterate samples
You can iterate through samples by using
```python
samples = Samples('samples.json')
for sample in samples:
    #do something
    continue
```

## API Reference
### init
*Method signature:*
```python
def __init__(samples_list_or_path, name="", sample_input_key="input", sample_output_key="target", validate_samples_len=False): 
```
Initializes a Samples object. Takes a list of samples or a path to a file containing samples, a name for the Samples object, the key for the input data in each sample, the key for the target data in each sample, and a flag indicating whether to check the validity of the samples.

### len
*Method signature:*
```python
def __len__():
```
Returns the number of samples in the dataset.

### iter
*Method signature:*
```python
def __iter__():
```
Returns an iterator over the samples.

### next
*Method signature:*
```python
def __next__():
```
Returns the next sample in the iterator. Raises a StopIteration exception once all items are returned.

### str
*Method signature:*
```python
def __str__():
```
Returns a string representation of the Samples object.

### load_samples
*Method signature:*
```python
def load_samples(samples_json_file):
```
Loads samples from a JSON file. Takes the path to the JSON file containing the samples and returns a list of samples loaded from the file.

### validate_samples
*Method signature:*
```python
def validate_samples(desired_len=0):
```
Checks the validity of the samples. Raises a KeyError if a sample is missing either "input" or "target" data, and `desired_len` is set to value other than `0` a `ValueError` is raised if the length of the input and target data in a sample do not match the `desired_len`.

### get_all_samples
*Method signature:*
```python
def get_all_samples():
```
Returns all samples in the dataset.

### shuffle
*Method signature:*
```python
def shuffle(times=1):
```
Shuffles the samples a specified number of times. Takes the number of times to shuffle the list of samples.

### split_samples_by_proportions
*Method signature:*
```python
def split_samples_by_proportion(proportions_list=[0.7, 0.2, 0.1], names_list=["train", "eval", "test"], shuffle=1):
```
Splits the samples into multiple subsets based on the given proportions and returns a list of Samples objects. Takes a list of proportions for each subset, a list of names for each subset, and a flag to shuffle the samples before splitting. Raises a ValueError if a split size is 0.
The proportions get normalized before splitting, so they don't need to add up to one. 
In this sense using `proportion_list = [2, 1, 1]` gives the same result as using `proportions_list = [0.5, 0.25, 0.25]`

## License
GNU AGPLv3 2023, [laelhalawani@gmail.com](https://github.com/laelal.halawani).

## Contributing
Any and all is welcome, thank you!