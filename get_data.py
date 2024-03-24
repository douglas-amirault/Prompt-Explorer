import nltk
from src.data_loader import DataLoader

dl = DataLoader("poloclub/diffusiondb", "2m_first_5k")

dl.download_dataset(5000)

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")