from datetime import date


# Override default parameters if needed

# Area of the listing
area = ""
# Type (Room / Studio / Apartment)
apartment_type = "Apartment"
# Maximum rent cutoff
max_rent = ""
# Number of apartments to check for
nb_per_page = 50
# Data since you were in queue in (YYYY, MM, DD) format
member_since = date(2001, 10, 31)
# Save the plot in the ./cache folder or display
save_plot = True
# Display dataframe of the current status or not
verbose = True


# Execute
if __name__ == "__main__":
    if save_plot:
        import matplotlib
        matplotlib.use("Agg")

    from sssb import SSSBParser
    if 'parser' not in vars():
        parser = SSSBParser(cache_type="h5")

    tree = parser.get(
        'etree',
        area, apartment_type, max_rent, nb_per_page
    )
    parser.make_df(tree)
    if verbose:
        print(parser.df)

    change_in_data = parser.make_df_hist()
    if change_in_data:
        parser.member_since = member_since
        parser.plot_hist(save_plot)
        parser.save()
