import pandas as pd
import numpy as np

df = pd.read_csv('Data Sets/store_transactions_2021-2022.csv',
    dtype={'ReturnedQty': str,
            'PromotionNum' : str,
            'TruckSaleFlg' : int,
            'AccountType' : str,
            'UPC' : str,
            'IAProgramID' : str
            },
    low_memory=False
    )

df.to_parquet('Data Sets/Transactions', partition_cols='SrcStoreNum')