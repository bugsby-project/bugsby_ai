# Generating the label dataset

The label dataset contains issues from several open-source projects, obtained via the GitHub REST API.

This dataset can be generated by running the `createDataset.py` Python script with the command
`python createDataset.py <token>`. Due to the APIs limitations in terms of number of requests that can be made by
unauthenticated users, a personal access token is required, which is given to the script as a command line parameter.
Please refer to
the [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
for creating a personal access token.

## The components of the dataset

At the time of writing, the distribution of issues of the following GitHub projects in terms of label is:

| Project              | # Bug | # Documentation | # Enhancement | # Invalid | # Won't fix |
|----------------------|-------|-----------------|---------------|-----------|-------------|
| [RxJava](https://github.com/ReactiveX/RxJava)               |   732 |             564 |           776 |        58 |           7 |
| [netty](https://github.com/netty/netty)                |  2659 |             126 |          1135 |         0 |         108 |
| [Guava](https://github.com/google/guava)                |   464 |              91 |           580 |       174 |         420 |
| [Storio](https://github.com/pushtorefresh/storio)               |    79 |               0 |           602 |         0 |           6 |
| [ChartJs](https://github.com/chartjs/Chart.js)              |  2402 |             785 |          1332 |         0 |          92 |
| [Tensorflow](https://github.com/tensorflow/tensorflow)           |     0 |               0 |             0 |       110 |           0 |
| [Geany](https://github.com/geany/geany)                |     0 |               0 |             0 |       148 |           0 |
| [Java Design Patterns](https://github.com/iluwatar/java-design-patterns) |     0 |               0 |             0 |        14 |          67 |

Please note that some projects have different names for the same label type. For example, labels such as *defect* or *type: bug* are treated as *Bug*.

Due to the fact that GitHub considers pull-requests as issues, the `createDataset.py` script removes them from the dataset.
After this process, the distribution of issues is the following:

| # Bug | # Documentation | # Enhancement | # Invalid | # Won't fix |
|-------|-----------------|---------------|-----------|-------------|
| 4157  | 532             | 2417          | 338       | 423         |
