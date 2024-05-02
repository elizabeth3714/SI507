import pandas as pd 
import numpy as np

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
        # Fill in NAs
        for i in properties.columns:
            # Calculate the distribution of non-NaN values
            distribution = properties[i].value_counts(normalize=True)

            # Get the NaN indices in the column
            nan_indices = properties[properties[i].isnull()].index

            # Randomly select values according to the distribution to fill NaNs
            random_choices = np.random.choice(distribution.index, size=len(nan_indices), p=distribution.values)

            # Fill in the NaN values in the DataFrame
            properties.loc[nan_indices, i] = random_choices        

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
            
            # find properties with similar features
            for col in property_list.columns:
                if curr_property[col].iloc[0] == property_list[col].iloc[i]\
                    and curr_property['mls_id'][0] != property_list['mls_id'][i]:
                    similarity_score += 1
                else:
                    pass
            # search the best match that have the most common features
            if similarity_score > similarity_score_max:
                similarity_score_max = similarity_score
                recommd_property = property_list.iloc[i].to_dict()
                recommd_property = {key: [value] for key, value in recommd_property.items()}

            else:
                pass

        return recommd_property, similarity_score_max


    def generateAdjList(self):
        property_list = self.load_properties()
        property_list['price_range'] = 'price_' + property_list['price_range'].astype(str)
        property_list['sqft'] = 'sqft_' + property_list['sqft'].astype(str)

        adjList = {}
        # Extract Home IDs; assuming first column is 'mls_id'
        homeID = property_list['mls_id'].tolist()

        # Prepare the adjacency list dictionary
        adjList = {id: set() for id in homeID}

        # We will exclude some columns from creating connections
        excluded_columns = ['mls_id', 'street', 'latitude', 'longitude', 'primary_photo', 'property_url']
        included_columns = [col for col in property_list.columns if col not in excluded_columns]

        # Creating a graph mapping from features to home IDs
        feature_to_ids = {}
        for col in included_columns:
            for idx, value in enumerate(property_list[col]):
                # feature = f"{col}_{value}"
                feature = value
                if feature not in feature_to_ids:
                    feature_to_ids[feature] = set()
                feature_to_ids[feature].add(homeID[idx])
        # id_to_feature = {(id, feature) for feature, ids in feature_to_ids.items() for id in ids}

        # homeID-shared_feature-homeID as the graph structure
        for feature, mlsID in feature_to_ids.items():
            for mlsID1 in mlsID:
                for mlsID2 in mlsID:
                    if mlsID1 != mlsID2:
                        adjList[mlsID1].add((mlsID2, feature))      

        adjList2 = {id: {} for id in homeID}
        # Linking all IDs sharing the same feature and counting co-occurrences
        for ids in feature_to_ids.values():
            id_list = list(ids)
            for i in range(len(id_list)):
                for j in range(i + 1, len(id_list)):
                    id1, id2 = id_list[i], id_list[j]
                    if id2 not in adjList2[id1]:
                        adjList2[id1][id2] = 0
                    if id1 not in adjList2[id2]:
                        adjList2[id2][id1] = 0
                    adjList2[id1][id2] += 1
                    adjList2[id2][id1] += 1

        # Debug: print an example to see the adjacency list
        # print(adjList[homeID[0]])  # Print adjacencies for the first ID for testing
        # return feature_to_ids
        # return id_to_feature
        # return adjList[homeID[0]], adjList2
        return adjList, adjList2
        
    def query_co_occurrence(self, adjList2, id1, id2):
        """
        Query the adjacency list for the count of co-occurrences between two home IDs.
        """
        if id1 in adjList2 and id2 in adjList2[id1]:
            return adjList2[id1][id2]
        elif id2 in adjList2 and id1 in adjList2[id2]:
            return adjList2[id2][id1]
        else:
            return 0  # No co-occurrence found

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

    # adjList, n_cooccurence = generateAdjList()
    # print(adjList['PAPH2347528'])
    # query_co_occurrence(n_cooccurence, 'PAPH2347528', 'PAPH2345718')


if __name__ == "__main__":
    main()