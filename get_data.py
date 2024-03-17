from src.data_loader import DataLoader

dl = DataLoader("poloclub/diffusiondb", "2m_all")

dl.download_dataset(2_000_000)
