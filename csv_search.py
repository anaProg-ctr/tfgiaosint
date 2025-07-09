"""
This module implements a function to read a CVS file and search in specific 
columns for char sequences.
"""
import pandas as pd

def csv_search(csv_file, search_cols, search_terms, show_n_cols = None, show_m_chars = None):
    """
    Search in a CSV file for char squences in specific columns.

    Args:
        csv_file (str): CSV file to process,
        search_cols (list): list of the name of columns to perform the 
                            search in,
        search_terms (list): list of char sequences to search for,
        show_n_cols (int, optional): to set the number of columns to show 
                                     from the first in the file
        show_m_chars (int, optional): limits the number of char to show, in
                                      case that show_n_cols is given
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"'{csv_file}' loaded.")
        print("Columns:", df.columns.tolist())

        for col in search_cols:
            if col not in df.columns:
                print(f"\nError: column '{col}' does not exist.")
                return

        final_test_result = pd.Series([False] * len(df), index = df.index)
        terms_by_rows = [''] * len(df)
        for term in search_terms:
            for col in search_cols:

                test_col_term = df[col].astype(str).str.contains(term, case = False, na = False)
                final_test_result = final_test_result | test_col_term
                for i, found in enumerate(test_col_term):
                    if found:
                        if term not in terms_by_rows[i]:
                            if terms_by_rows[i]:
                                terms_by_rows[i] += f", {term}"
                            else:
                                terms_by_rows[i] = term

        results = df[final_test_result].copy()
        terms_str = ", ".join(search_terms)
        if not results.empty:
            serie_of_terms = pd.Series(terms_by_rows, index = df.index)
            results['Found'] = serie_of_terms[final_test_result]
            df_2_show = results.copy()
            if show_n_cols is not None and show_n_cols > 0:
                list_of_cols = df_2_show.columns.tolist()
                select_cols = list_of_cols[:show_n_cols]
                if 'Found' in list_of_cols and 'Found' not in select_cols:
                    select_cols.append('Found')
                df_2_show = df_2_show[select_cols]

                if show_m_chars is not None and show_m_chars >= 0:
                    for i, col in enumerate(df_2_show.columns):
                        if i < show_n_cols-1:
                            if df_2_show[col].dtype == 'object':
                                df_2_show[col] = df_2_show[col].astype(str).apply(
                                    lambda x: x[:show_m_chars] + '...'
                                        if len(x) > show_m_chars else x
                                )
            print(f"\n'{terms_str}' found in columns '{search_cols}':")
            print(df_2_show.to_csv(index = False, sep=',', header = True))
        else:
            print("No results.")

    except FileNotFoundError:
        print(f"Error: file '{csv_file}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: file '{csv_file}' is empty.")
    except Exception as e:
        print(f"Unexpected error: {e}")
