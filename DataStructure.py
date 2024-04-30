import pandas as pd 

class HomeSearch:
    def __init__(self, file_path):
        self.file_path = file_path
        self.property_list = self.load_properties()

    def load_properties(self):
        """
        Load properties from csv file
        """
        # properties = pd.read_csv('HomeHarvest_20240425_130853_philly_forsale90days.csv')
        # properties = pd.read_csv('HomeHarvest_20240425_180641_philly_forsale365days.csv')
        # properties = pd.read_csv('HomeHarvest_20240425_184034_philly_forrent365days.csv')
        properties = pd.read_csv(self.file_path)

        bins = [0, 10000, 50000, 100000, 300000, 500000, 700000, 1000000, 100000000000000]
        properties['price_range'] = pd.cut(properties['list_price'], bins, labels= [1,2,3,4,5,6,7,8])
                                    # ['0-10k', '10k-50k', '50k-100k', '100k-300k', '300k-500k', '500k-700k', '700k-1M', '1M+'])

        bins = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000,  100000000000000]
        properties['sqft'] = pd.cut(properties['sqft'], bins, labels= [1,2,3,4,5,6,7,8,9,10,11])

        property_id = properties[['mls_id']]
        property_info = properties[['zip_code', 'beds', 'price_range', 'style', 'sqft', 'neighborhoods',
                                    'street', 'latitude', 'longitude', 'primary_photo', 'property_url']]
        property_list = properties[['mls_id', 'zip_code', 'beds', 'price_range', 'style', 'sqft', 'neighborhoods',
                                    'street', 'latitude', 'longitude', 'primary_photo', 'property_url']]
        for i in property_list.columns:
            property_list[i] = property_list[i].astype(str)
        # return property_id, property_info, property_list
        return property_list

    def recommendation(self, curr_property):
        property_list = self.load_properties()
        property_list = property_list.sample(frac=1)
        # Generate recommendation based on similarity score
        n_rows = len(property_list.index)
        n_cols = property_list.shape[1]
        similarity_score_max = 0
        recommd_property = None

        for i in range(0, n_rows-1):
            similarity_score = 0

            # Iterate through each column
            # for j in range(1, n_cols-1):
            #     # Add to similarity score if column value is the same 
            #     # (aka properties sharing the same feature)
            #     if curr_property.iloc[j] == property_list.iloc[i, j] \
            #         and curr_property.iloc[7] != property_list.iloc[i, 7]: # can't be the same property
            #         similarity_score += 1
            
            for col in property_list.columns:
                if curr_property[col].iloc[0] == property_list[col].iloc[i]\
                    and curr_property['mls_id'][0] != property_list['mls_id'][i]:
                    similarity_score += 1
                else:
                    pass
            
            if similarity_score > similarity_score_max:
                similarity_score_max = similarity_score
                recommd_property = property_list.iloc[i].to_dict()
                recommd_property = {key: [value] for key, value in recommd_property.items()}

            else:
                pass

        return recommd_property, similarity_score_max

#    @staticmethod
def main():
    """
    Main function that loads the properties and prints a sample recommendation.
    """
    # file_path = 'HomeHarvest_20240425_184034_philly_forrent365days.csv'
    # homesearch = HomeSearch(file_path)
    # property_list = homesearch.load_properties()
    # # Assume curr_property is the first property from the dataset for demo purposes
    # curr_property = property_list.iloc[3]
    # recommendation, score = homesearch.recommendation(curr_property)
    # print("Recommended Property:", recommendation)
    # print("Similarity Score:", score)


if __name__ == "__main__":
    main()