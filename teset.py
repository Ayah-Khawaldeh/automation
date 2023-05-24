import json


if __name__ == '__main__':
    json_file = open('configs.json')
    configs = json.load(json_file)

    print(configs['length_of_article'])