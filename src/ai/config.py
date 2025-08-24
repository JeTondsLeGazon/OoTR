from pydantic_settings import BaseSettings


class DeepQNetworkSettings(BaseSettings):
    no_exploration_after_n_steps: int = 10000

    discount_factor: float = 0.95
    learning_rate: float = 0.001
    exploration_rate = 0.15

    memory_size: int = 1000000
    batch_size: int = 20
    memory_interval: int = 20
