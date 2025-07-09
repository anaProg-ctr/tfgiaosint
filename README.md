# tfgiaosint

In this repository you will find a Python file I have used to help me in my Degree Project.

It is a function with the following signature:

```python
csv_search(csv_file, search_cols, search_terms, show_n_cols = None, show_m_chars = None)
```

Its arguments are:

```
        csv_file (str): CSV file to process,
        search_cols (list): list of the name of columns to perform the 
                            search in,
        search_terms (list): list of char sequences to search for,
        show_n_cols (int, optional): to set the number of columns to show 
                                     from the first in the file
        show_m_chars (int, optional): limits the number of char to show, in
                                      case that show_n_cols is given
```
