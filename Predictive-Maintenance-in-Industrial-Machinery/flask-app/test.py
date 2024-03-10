import random
import pandas as pd
from time import time
import matplotlib.pyplot as plt
from ml_model import ml_function

def test_df(n):
    columns = ["Type", "Air temperature [K]", "Process temperature [K]", 
    "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]", "Power"]
    data = []

    for _ in range(n):
        row = [
            random.choice(['M', 'L', 'H']),
            random.randint(250, 350),
            random.randint(300, 320),
            random.randint(1100, 3000),
            random.randint(3, 80),
            random.randint(0, 255),
            random.randint(10500, 99990)
        ]
        data.append(row)

    return pd.DataFrame(data, columns=columns)

df = test_df(1000)
df.to_csv('test.csv', index=False)
failear_df = ml_function(df)
print(df)
print()
print(failear_df)

n_rows = range(1, 10002, 50)
time_taken = []
print()
for i in n_rows:
    start = time()
    df = test_df(i)
    ml_function(df)
    diff = time()-start
    print(f'\rn_rows={i}, time_taken={diff:.5f}  ', end='', flush=True)
    time_taken.append(diff)
print()
plt.plot(n_rows, time_taken)
plt.title('Time Complexity')
plt.xlabel('Number of rows')
plt.ylabel('Time Taken(s)')
plt.savefig('time-complexity.png')
plt.close()