import matplotlib
import matplotlib.style
import matplotlib.pyplot as plt
from chronokit.preprocessing.dataloader import DataLoader

def plot_decomp(trend, seasonal, remainder, method="add", figsize=(12,8), colors=None, style=None):
    """
    Utility function for plotting time series decomposition results
    
    Arguments:

    *trend (array_like): Trend component of the decomposition
    *seasonal (array_like): Seasonal component of the decomposition
    *remainder (array_like): Remainders of the decomposition
    *method Optional[str]: Method of the decomposition, "add" or "mul". If not one of these, will be taken as "add".
    *figsize Optional[tuple]: Size of the plot
    *colors Optional[iterable]: Colors of the lines/points on the plot
    *style Optional[str]: Style of the plot 'https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html'
    """

    if style:
        assert(type(style) == str), "Provide style as a string"
        matplotlib.style.use(style)
    
    use_colors = {"trend": "blue", "seasonal": "blue", "remainder": "blue"}

    if colors:
        try:
            iter(colors)
        except TypeError:
            raise TypeError("Provide colors as an iterable")
        
        if type(colors) == dict:
            for key in colors:
                assert(key in list(use_colors.keys())), f"Ensure that keys in colours dictionary are {list(use_colors.keys())}"
                use_colors[key] = colors[key]

        else:
            for ind, c in enumerate(colors):
                use_colors[list(use_colors.keys())[ind]] = c

    trend = DataLoader(trend).to_numpy()
    seasonal = DataLoader(seasonal).to_numpy()
    remainder = DataLoader(remainder).to_numpy()

    if seasonal.ndim > 1:
        num_seasonals = seasonal.shape[0]
    else:
        num_seasonals = 1
    
    fig, axes = plt.subplots(2+num_seasonals, 1, figsize=figsize)
    ax_trend, ax_remainder = axes[0], axes[-1]     
    ax_trend.plot(range(len(trend)), trend, color=use_colors["trend"])
    ax_trend.set_ylabel("Trend")

    if num_seasonals > 1:
        for i in range(num_seasonals):
            cur_seasonal = seasonal[i]
            ax_seasonal = axes[i+1]
            ax_seasonal.plot(range(len(cur_seasonal)), cur_seasonal, color=use_colors["seasonal"])
            ax_seasonal.set_ylabel(f"Seasonal_{i}")
    else:
        ax_seasonal = axes[1]
        ax_seasonal.plot(range(len(seasonal)), seasonal, color=use_colors["seasonal"])
        ax_seasonal.set_ylabel(f"Seasonal")

    ax_remainder.scatter(range(len(remainder)), remainder, color=use_colors["remainder"])
    line_val = 1 if method == "mul" else 0
    ax_remainder.plot(range(len(remainder)), [line_val for i in remainder], color="black")
    ax_remainder.set_ylabel("Remainder")
    plt.show()
        

def plot_train_test_split(train_data, test_data, val_data=None, figsize=(12,8), title: str =None, colors=None, style=None):
    """
    Utility function for plotting train test split
    
    Arguments:

    *train_data (array_like): Training data of the split
    *test_data (array_like): Test data of the split
    *val_data (Optional[array_like]): Val data of the split if data is splitted as train/val/test
    *figsize (Optional[tuple]): Size of the plot
    *title (Optional[str]): Title of the plot
    *colors (Optional[iterable]): Colors of the lines/points on the plot
    *style (Optional[str]): Style of the plot 'https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html'
    """
    
    assert (type(title) == "str" or title is None), "Plot title must be a string"

    if style:
        assert(type(style) == str), "Provide style as a string"
        matplotlib.style.use(style)
    
    use_colors = {"train": "blue", "val": "orange", "test": "red"}

    if colors:
        try:
            iter(colors)
        except TypeError:
            raise TypeError("Provide colors as an iterable")
        
        if type(colors) == dict:
            for key in colors:
                assert(key in list(use_colors.keys())), f"Ensure that keys in colours dictionary are {list(use_colors.keys())}"
                use_colors[key] = colors[key]

        else:
            for ind, c in enumerate(colors):
                use_colors[list(use_colors.keys())[ind]] = c

    train = DataLoader(train_data).to_numpy()
    test = DataLoader(test_data).to_numpy()

    if val_data:
        val = DataLoader(val_data).to_numpy()
        plt.figure(figsize=figsize)
        plt.plot(range(len(train)), train, label="Train", color=use_colors["train"])
        plt.plot(range(len(train), len(train)+len(val_data)), val, label="Validation", color=use_colors["val"])
        plt.plot(range(len(train+val_data), len(train)+len(val_data)+len(test_data)), test, label="Test", color=use_colors["test"])
        plt.legend(loc="best")
        plt.title(title)
        plt.show()
       
    else:
        plt.figure(figsize=figsize)
        plt.plot(range(len(train)), train, label="Train", color=use_colors["train"])
        plt.plot(range(len(train), len(train)+len(test)), test, label="Test", color=use_colors["test"])
        plt.legend(loc="best")
        plt.title(title)
        plt.show()
    