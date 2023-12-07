## Data Processing Project

### Project Description

This project solves test task using the pandas library.
The project uses a provided .csv file as the database and 
performs data processing based on specific input requests.

#### This app generates two outputs: 
* List of all sources for request.
* Filtered and grouped data for each source.

**Technologies Used:**

* Python 3.11
* pandas library
* numpy library

### Input Format

The input is a python dict containing two keys: `code1` and `code2`.

Example:

```
{
  "code1": "shA",
  "code2": "W"
}
```

### Output Format

The output consists of two parts:

**1. List of Sources:**

A dictionary where the key is a tuple of `(code1, code2)`, and the value is a list of all possible sources for that combination.

**2. Filtered and Grouped Data:**

A list of dictionaries, where each dictionary has a key that is a tuple of `(code1, code2, source)`, and the value is a list of data rows for that specific combination. Each data row includes the following columns:

* updateDate
* code1
* code2
* code3
* value
* siCode
* bitCode

### How to Run

```shell
git clone https://github.com/MarianKovalyshyn/code-converter.git
cd code-converter/
python -m venv venv
source venv/bin/activate (MacOS)
venv\Scripts\activate (Windows)
pip install -r requirements.txt
python main.py
```

This will print the two outputs for a sample request
(you can change the request in the `sample_request` variable)
