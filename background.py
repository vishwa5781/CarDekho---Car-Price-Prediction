import pandas as pd
import ast
import json

def structured_data(df):
    def parse_list_dictionary(df,feature):
        def flatten_specifications(spec_list):
            parsed_data = {}
            for spec in spec_list:
                key_name = spec.get('key', '').replace(" ", "_").lower()
                parsed_data[f"{key_name}"] = spec.get('value', '')
            return parsed_data

        specs_df = df[feature].apply(flatten_specifications).apply(pd.Series)

        final_df = pd.concat([df.drop(feature, axis=1), specs_df], axis=1)

        return final_df
    def parse_json_field(field):
        try:
            return ast.literal_eval(field) if pd.notna(field) else {}
        except (ValueError, SyntaxError):
            return {}


    def feature_dictionary(df, feature, data):
    
        df['top_flat'] = df[feature].apply(lambda x: [item['value'] for item in x])

        def expand_data(data_list):
            result = {}
            for entry in data_list:
                heading = entry['heading']
                values = [item['value'] for item in entry['list']]
                result[heading] = values
            return result

        expanded_data = df[data].apply(expand_data).apply(pd.Series)

        df = pd.concat([df, expanded_data], axis=1)

        df = df.drop(columns=[feature, data])

        def unique_first_occurrence(row):
            seen = set()
            combined_list = []
            for col in row:
                if isinstance(col, list):
                    for item in col:
                        if item not in seen:
                            seen.add(item)
                            combined_list.append(item)
            return combined_list

        df['combined_unique'] = df.apply(unique_first_occurrence, axis=1)
        df['feature'] = df['combined_unique'].apply(len)

        return df
    def spec_data_parsing(df):

        df['data'] = df['data'].apply(lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else x)

        def extract_values(data, heading, subheading):
            for item in data:
                if item['heading'] == heading and item['subHeading'] == subheading:
                    return {entry['key']: entry['value'] for entry in item['list']}
            return {}

        df['engine_transmission'] = df['data'].apply(lambda x: extract_values(x, 'Engine and Transmission', 'Engine'))
        df['dimensions_capacity'] = df['data'].apply(lambda x: extract_values(x, 'Dimensions & Capacity', 'Dimensions'))
        df['miscellaneous'] = df['data'].apply(lambda x: extract_values(x, 'Miscellaneous', 'Miscellaneous'))

        df = pd.concat([df.drop(columns=['data']),
                        df['engine_transmission'].apply(pd.Series).add_prefix('engine_'),
                        df['dimensions_capacity'].apply(pd.Series).add_prefix('dimension_'),
                        df['miscellaneous'].apply(pd.Series).add_prefix('misc_')], axis=1)
        df=df.drop(['engine_transmission','dimensions_capacity','miscellaneous'],axis=1)

        return df
    
    df['new_car_detail'] = df['new_car_detail'].apply(parse_json_field)
    df['new_car_overview'] = df['new_car_overview'].apply(parse_json_field)
    df['new_car_feature'] = df['new_car_feature'].apply(parse_json_field)
    df['new_car_specs'] = df['new_car_specs'].apply(parse_json_field)

    details_df = pd.json_normalize(df['new_car_detail'])
    details_df = pd.concat([details_df.iloc[:, :13],details_df.iloc[:, -2:]], axis=1)

    overview_df = pd.json_normalize(df['new_car_overview'])
    overview_df=overview_df.drop('heading',axis=1)
    overview_df=overview_df.drop('bottomData',axis=1)
    overview_df=parse_list_dictionary(overview_df,'top')

    feature_df = pd.json_normalize(df['new_car_feature'])
    feature_df=feature_df.drop('heading',axis=1)
    feature_df=feature_df.drop('commonIcon',axis=1)
    feature_df=feature_dictionary(feature_df,'top','data')
    feature_df=feature_df.iloc[:, -1:]

    specs_df = pd.json_normalize(df['new_car_specs'])
    specs_df=specs_df.drop('heading',axis=1)
    specs_df=specs_df.drop('commonIcon',axis=1)
    specs_df=parse_list_dictionary(specs_df,'top')
    specs_df=spec_data_parsing(specs_df)

    final_df = pd.concat([ details_df, overview_df, feature_df, specs_df], axis=1)

    return final_df