import pandas as pd
import numpy as np

if __name__ == "__main__":
    error_log = pd.read_csv("error_log.csv")

    lengths = error_log["Length"]
    lengths = list(dict.fromkeys(lengths))
    lengths.sort()

    algorithms = error_log["Algorithm"]
    algorithms = list(dict.fromkeys(algorithms))

    distributions = error_log["Distribution"]
    distributions = list(dict.fromkeys(distributions))
    print(lengths, algorithms, distributions)

    changepoint_count = str(error_log["Error"][0]).count("|") + 1

    errors_out = open("errors.csv", "w")

    # Make Header
    errors_out.write(",")
    for _, dist in enumerate(distributions):
        errors_out.write(dist + "," * len(algorithms))
    errors_out.write("\n")

    errors_out.write(",")
    for _, dist in enumerate(distributions):
        errors_out.write(f"Average Error" + "," * len(algorithms))
    errors_out.write("\n")

    errors_out.write("Length,")
    for _, dist in enumerate(distributions):
        for _, alg in enumerate(algorithms):
            errors_out.write(alg + ",")
    errors_out.write("\n")

    for _, length in enumerate(lengths):
        errors_out.write(str(length) + ",")

        for _, dist in enumerate(distributions):
            for _, alg in enumerate(algorithms):
                errors = error_log[(error_log.Length == length) & (error_log.Algorithm == alg) & (error_log.Distribution == dist)]
                error_list = []
                for _, error_iteration in errors.iterrows():
                    if isinstance(error_iteration.Estimates, float) and np.isnan(error_iteration.Estimates):
                        continue

                    error_array = [error_iteration.Estimates]
                    if  isinstance(error_iteration.Estimates, str):
                        error_array = error_iteration.Estimates.split("|")

                    changepoint_array = [error_iteration.Changepoints_rel]
                    if  isinstance(error_iteration.Changepoints_rel, str):
                        changepoint_array = error_iteration.Changepoints_rel.split("|")

                    estimates_array = np.sort([float(x) for x in error_array])
                    changepoints_array = np.sort([float(x) for x in changepoint_array])

                    if len(estimates_array) != len(changepoints_array):
                        error_list.append(1)
                        continue

                    error_list.append(np.sum(np.abs(estimates_array - changepoints_array)) / (float(length) * len(estimates_array)))
                    print(error_list[-1])

                if len(error_list) != 0:
                    errors_out.write(str(np.mean(error_list)))
                else:
                    errors_out.write("1")
                errors_out.write(",")



        errors_out.write("\n")

    errors_out.close()

