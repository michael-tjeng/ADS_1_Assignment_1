import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Load and preprocess sales data from a CSV file.

    The preprocessing steps include:
    - Decoding the file using 'latin1' encoding.
    - Converting the 'InvoiceDate' to datetime objects and dropping rows with
    invalid dates.
    - Calculating the total sales by multiplying 'Quantity' and 'UnitPrice'.
    - Setting the 'InvoiceDate' as the index of the DataFrame.

    Parameters:
    - file_path (str): The file system path to the CSV file containing sales
    data.

    Returns:
    - pd.DataFrame: The preprocessed sales data with 'InvoiceDate' as the
    index.
    """
    data = pd.read_csv(file_path, encoding='latin1')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
    data = data.dropna(subset=['InvoiceDate'])
    data['TotalSales'] = data['Quantity'] * data['UnitPrice']
    data.set_index('InvoiceDate', inplace=True)
    return data


def get_monthly_sales(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total sales per month for each country from the sales data.

    The function groups the data by 'Country' and resamples it to monthly 
    frequency, aggregating the 'TotalSales' for each month.

    Parameters:
    - data (pd.DataFrame): The preprocessed sales data with 'InvoiceDate' as 
    the index.

    Returns:
    - pd.DataFrame: A DataFrame with columns 'Country', 'InvoiceDate', and 
    'TotalSales', showing the total sales for each country per month.
    """
    return data.groupby('Country').resample('M')[
        'TotalSales'].sum().reset_index()


def plot_total_monthly_sales(monthly_sales: pd.DataFrame) -> None:
    """
    Plot and save a line chart of total monthly sales over time.

    This function takes the monthly sales data, aggregates it to find total 
    sales for each month, and plots a line chart showing the trend of sales 
    over time. The chart is saved as a PNG file.

    Parameters:
    - monthly_sales (pd.DataFrame): DataFrame containing monthly sales data 
    with 'InvoiceDate' and 'TotalSales' columns.

    Saves:
    - A PNG file of the plot with filename 'total_monthly_sales.png' to the 
    current directory.
    """
    plt.figure(figsize=(10, 7))
    total_monthly_sales = monthly_sales.groupby('InvoiceDate')[
        'TotalSales'].sum()
    plt.plot(total_monthly_sales.index,
             total_monthly_sales.values, label='Total Sales')
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.title('Total Monthly Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales (£)')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('total_monthly_sales.png', dpi=300)
    plt.show()


def get_sales_by_hour(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total sales per hour from the sales data.

    This function adds an 'Hour' column based on the 'InvoiceDate' index and 
    groups the data by this hour to calculate the total sales for each hour of 
    the day.

    Parameters:
    - data (pd.DataFrame): The preprocessed sales data with 'InvoiceDate' as 
    the index.

    Returns:
    - pd.DataFrame: A DataFrame with columns 'Hour' and 'TotalSales', 
    representing the total sales for each hour of the day.
    """
    data['Hour'] = data.index.hour
    return data.groupby('Hour')['TotalSales'].sum().reset_index()


def plot_sales_by_hour(sales_by_hour: pd.DataFrame) -> None:
    """
    Plot and save a bar chart of sales by hour of the day.

    This function creates a bar chart to visualize the total sales for each 
    hour. The chart is saved as a PNG file.

    Parameters:
    - sales_by_hour (pd.DataFrame): DataFrame containing sales data aggregated 
    by hour with columns 'Hour' and 'TotalSales'.

    Saves:
    - A PNG file of the plot with filename 'sales_by_hour.png' to the current 
    directory.
    """
    plt.figure(figsize=(10, 7))
    plt.bar(sales_by_hour['Hour'],
            sales_by_hour['TotalSales'], color='skyblue')
    plt.title('Sales by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Sales (£)')
    plt.xticks(range(24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('sales_by_hour.png', dpi=300)
    plt.show()


def plot_total_sales_by_country(data: pd.DataFrame) -> None:
    """
    Plot and save an exploding pie chart of total sales by country.

    This function calculates the total sales for each country, sorts them in 
    descending order, and plots a pie chart for the top 5 countries with all 
    other countries aggregated into a single category. The chart is saved as a 
    PNG file.

    Parameters:
    - data (pd.DataFrame): The preprocessed sales data.

    Saves:
    - A PNG file of the plot with filename 'total_sales_by_country.png' to the 
    current directory.
    """
    total_sales_by_country = data.groupby(
        'Country')['TotalSales'].sum().sort_values(ascending=False)
    top_5_countries = total_sales_by_country.head(5)
    other_countries_sum = total_sales_by_country[5:].sum()
    pie_data = top_5_countries.append(
        pd.Series(other_countries_sum, index=['Other Countries']))

    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    colors = plt.cm.Paired(range(len(pie_data)))

    plt.figure(figsize=(10, 7))
    wedges, _ = plt.pie(pie_data, startangle=140, explode=explode,
                        colors=colors, textprops=dict(color="w"))
    labels = [
        f"{label}: {perc:.1f}% ({amount:,.0f} £)"
        for label, perc, amount in zip(
            pie_data.index, 100 * pie_data / pie_data.sum(), pie_data
        )
    ]
    plt.legend(wedges, labels, title="Countries",
               loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
    plt.title('Total Sales by Country')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('total_sales_by_country.png', dpi=300, bbox_inches='tight')
    plt.show()

# main program
data = load_and_preprocess_data('data.csv')
monthly_sales = get_monthly_sales(data)
plot_total_monthly_sales(monthly_sales)
sales_by_hour = get_sales_by_hour(data)
plot_sales_by_hour(sales_by_hour)
plot_total_sales_by_country(data)
