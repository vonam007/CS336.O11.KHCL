import numpy as np
import cv2 as cv
import time
from pickle import dump, load
from PIL import Image
from scipy.spatial.distance import cosine
import cv2 as cv
from pathlib import Path
from tqdm import tqdm
from feature_extraction import VGG16_FE, Xception_FE, ResNet50_FE, MobileNetV2__FE, EfficientNetV2__FE, InceptionV3__FE
import argparse

def indexing():
    features_file_path = methods_folder_path / 'features.pkl'
    image_paths_file_path = methods_folder_path / 'images.pkl'

    if features_file_path.exists() and image_paths_file_path.exists():
        return  # Skip indexing if files already exist

    # Create features list and image paths list
    features, image_paths = [], []

    # Browse each image at images folder path with suffix .jpg
    for image_path in tqdm(sorted(images_folder_path.glob('*.jpg'))):
        try:
            # Open image at image path
            image = Image.open(image_path)

            # Extract feature from image
            feature = feature_extractor.extract(image)

            # Add feature to features list, image path to image paths list
            features.append(feature)
            image_paths.append(image_path)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue

    # Save features list and image paths list to the respective files
    with open(features_file_path, 'wb') as features_file, \
         open(image_paths_file_path, 'wb') as image_paths_file:
        dump(features, features_file)
        dump(image_paths, image_paths_file)

def retrieve_image(query_image, K=16) -> tuple:
    # Start counting time
    start = time.time()

    # Get features file path and image paths file path
    features_file_path = methods_folder_path / 'features.pkl'
    image_paths_file_path = methods_folder_path / 'images.pkl'

    # Open features file and image paths file to read
    features_file = open(features_file_path, 'rb')
    image_paths_file = open(image_paths_file_path, 'rb')

    # Load features list and image paths list from the respective opened files
    features = load(features_file)
    image_paths = load(image_paths_file)

    if isinstance(query_image, str):  # If query image is a path (string type)
        query_image = Image.open(query_image)  # Open query image at image path

    query_feature = feature_extractor.extract(query_image)  # Extract query feature from query image
    
    # Calculate cosine similarity scores between query feature and each feature in features list
    scores = [1 - cosine(query_feature, feature) for feature in features]


    # Get top K image ids with highest score
    topk_ids = np.argsort(scores)[::-1][:K]

    # Get image path with corresponding similarity from top K image ids
    ranked = [(image_paths[id], scores[id]) for id in topk_ids]

    # End counting time
    end = time.time()

    # Return top K relevant images and query time
    return ranked, end - start

def AP(predict, groundtruth, interpolated=False):
    precision = []
    recall = []
    correct = 0

    for id, (image, score) in enumerate(predict):
        if image.stem in groundtruth:
            correct += 1
            precision.append(correct / (id + 1))
            if interpolated:
                recall.append(correct / len(groundtruth))

    if interpolated:
        trec = [max((pr for pr, rc in zip(precision, recall) if rc >= R / 10), default=0) for R in range(11)]
        return np.mean(trec) if trec else 0

    return np.mean(precision) if precision else 0

def evaluating():
    results_folder_path = dataset_folder_path / 'results'
    if not results_folder_path.exists():
        results_folder_path.mkdir()

    result_file_path = results_folder_path / f'{dataset_folder_path.stem}_{method}_evaluation.txt'
    if result_file_path.exists():
        result_file_path.unlink()

    with open(result_file_path, 'a') as result_file:
        result_file.write('-' * 20 + 'START EVALUATING' + '-' * 20 + '\n\n')

        start = time.time()

        queries_file = sorted(groundtruth_folder_path.glob('*_query.txt'))

        nAPs, iAPs = [], []

        for id, query_file in enumerate(queries_file):
            groundtruth = []

            # Get groundtruth from files with 'good' and 'ok' results
            for suffix in ['good', 'ok']:
                with open(str(query_file).replace('query', suffix), 'r') as groundtruth_file:
                    groundtruth.extend(line.strip() for line in groundtruth_file.readlines())

            G = len(groundtruth)

            content = Path(query_file).read_text().strip().split()
            replace_str = 'oxc1_' if dataset_folder_path.stem == 'oxbuild' else ''
            image_name = content[0].replace(replace_str, '') + '.jpg'
            image_path = images_folder_path / image_name
            query_image = Image.open(image_path)

            rel_imgs, query_time = retrieve_image(query_image, G)

            nAP = AP(rel_imgs, groundtruth, interpolated=False)
            iAP = AP(rel_imgs, groundtruth, interpolated=True)

            nAPs.append(nAP)
            iAPs.append(iAP)

            result_file.write(f'+ Query {(id + 1):2d}: {Path(query_file).stem}.txt\n')
            result_file.write(' ' * 12 + f'Non - Interpolated Average Precision = {nAP:.2f}\n')
            result_file.write(' ' * 12 + f'Interpolated Average Precision = {iAP:.2f}\n')
            result_file.write(' ' * 12 + f'Query Time = {query_time:.2f}s\n')

        end = time.time()

        result_file.write('\n' + '-' * 19 + 'FINISH EVALUATING' + '-' * 20 + '\n\n')

        nMAP = np.mean(nAPs)
        iMAP = np.mean(iAPs)

        result_file.write(f'Total number of queries = {len(queries_file)}\n')
        result_file.write(f'Non - Interpolated Mean Average Precision = {nMAP:.2f}\n')
        result_file.write(f'Interpolated Mean Average Precision = {iMAP:.2f}\n')
        result_file.write(f'Evaluating Time = {(end - start):.2f}s')

    print(f'Evaluation result has been saved at {result_file_path}!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--d", help="Dataset", type=str, required=True)
    parser.add_argument("--m", help="Method for extracting features", type=str, required=True)
    parser.add_argument("--q", help="Path to the query image", type=str)
    parser.add_argument("--k", help="Number of retrieved images", type=int, default=16)
    parser.add_argument("--mode", help="Indexing/Retrieve/Evaluate", type=str, required=True)

    args = parser.parse_args()

    # Set defualt values
    dataset_name = args.d
    method = args.m
    if method == 'VGG16':
        feature_extractor = VGG16_FE()
    elif method == 'Xception':
        feature_extractor = Xception_FE()
    elif method == 'ResNet50':
        feature_extractor = ResNet50_FE()
    elif method == 'MobileNetV2':
        feature_extractor = MobileNetV2__FE()
    elif method == 'EfficientNetV2':
        feature_extractor = EfficientNetV2__FE()
    elif method == 'InceptionV3':
        feature_extractor = InceptionV3__FE()
    

    dataset_folder_path = Path('static/datasets') / dataset_name
    if not dataset_folder_path.exists():
        dataset_folder_path.mkdir()

    images_folder_path = dataset_folder_path / 'images'
    if not images_folder_path.exists():
        images_folder_path.mkdir()

    binary_folder_path = dataset_folder_path / 'binary'
    if not binary_folder_path.exists():
        binary_folder_path.mkdir()

    methods_folder_path = binary_folder_path / method
    if not methods_folder_path.exists():
        methods_folder_path.mkdir()

    groundtruth_folder_path = dataset_folder_path / 'groundtruth'
    if not groundtruth_folder_path.exists():
        groundtruth_folder_path.mkdir()

    if args.mode == 'Indexing':
        indexing()
    elif args.mode == 'Retrieve':
        result, time_taken = retrieve_image(args.q, args.k)
        print("Time taken:", time_taken)
        print(*result, sep='\n')
    elif args.mode == 'Evaluate':
        evaluating()













