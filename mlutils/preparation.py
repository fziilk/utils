import numpy as np
import pandas as pd
import shutil


def detect_outliers(df):
    cwo = list()
    df_cols = df.columns.tolist()
    numerical_columns = list()

    for column in df_cols:
        if df[column].dtype == np.int64:
            numerical_columns.append(column)

    for num_col in numerical_columns:
        skewness = df[num_col].skew()

        if skewness >= 1 or skewness <= -1:
            cwo.append(num_col)

    return cwo


def clean_dataset(df):
    cwo = detect_outliers(df)

    for o_col in cwo:
        Q1 = df[o_col].quantile(0.25)
        Q3 = df[o_col].quantile(0.75)
        IQR = Q3 - Q1
        whisker_width = 1.5

        outliers = df[
            (df[o_col] < Q1 - whisker_width * IQR)
            | (df[o_col] > Q3 + whisker_width * IQR)
        ]
        outlier_values = pd.DataFrame(outliers[o_col])
        outlier_values = outlier_values.values

        col_median = df[o_col].median()

        df[o_col] = df[o_col].replace(to_replace=outlier_values, value=col_median)
        
def merge_images(parent_dir):
    """
    input tree directory:
    > parent_dir
        > class 1
            > image 1
            > image 2
            > image n
        > class 2
            > image 1
            > image 2
            > image n
        > class n
            > image 1
            > image 2
            > image n

    output tree directory:
    > parent_dir
        > image 1
        > image 2
        > image 3
        > image 4
        > image 5
        > image 6
        > image 7
        > image 8
        > image n
    """
    classes = os.listdir(parent_dir)

    for subdir in classes:
        images = os.listdir(os.path.join(parent_dir, subdir))

        for image in images:
            try:
                print(f"moving \"{image}\"...")
                shutil.move(os.path.join(parent_dir, subdir, image), parent_dir)
            except Exception:
                pass

        shutil.rmtree(os.path.join(parent_dir, subdir))
